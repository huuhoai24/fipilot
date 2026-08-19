import json
import subprocess
import time
import urllib.request
from pathlib import Path

from azure.identity import DeviceCodeCredential

TENANT = "a7d5926e-252e-4db7-864e-195c5dc5f20e"
SUB = "73a4190e-3ee3-43ff-bf0a-40506e4fe7c1"
RG = "fipilot-rg"
LOCATION = "centralindia"
VM_NAME = "fipilot-gpu"
DNS_LABEL = f"fipilot-gpu-{int(time.time()) % 100000}"
SSH_KEY = str(Path.home() / ".ssh" / "fipilot_gpu")

if not Path(SSH_KEY).exists():
    print(f"[ssh] generating keypair -> {SSH_KEY}")
    Path(SSH_KEY).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", SSH_KEY, "-N", ""], check=True)
pub_key = Path(SSH_KEY + ".pub").read_text().strip()
print(f"[ssh] using public key: {pub_key[:60]}...")

cred = DeviceCodeCredential(tenant_id=TENANT)
token = cred.get_token("https://management.azure.com/.default").token

app_py = r'''import time
import uuid
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/opt/smartresume/model"

model = None
tokenizer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )
    model.eval()
    print("SmartResume model loaded on:", next(model.parameters()).device)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "SmartResume-Qwen3-0.6B"
    messages: list[ChatMessage]
    max_tokens: int = 256
    temperature: float = 0.1


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    messages = [m.model_dump() for m in req.messages]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            do_sample=True,
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    content = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": inputs["input_ids"].shape[1],
            "completion_tokens": int(outputs.shape[1] - inputs["input_ids"].shape[1]),
            "total_tokens": int(outputs.shape[1]),
        },
    }
'''

custom_script = f"""#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive
exec > /var/log/fipilot_setup.log 2>&1
echo "[1/5] apt update"
apt-get update -y
apt-get install -y python3.10-venv git curl
echo "[2/5] python venv + torch (CUDA)"
python3 -m venv /opt/smartresume
/opt/smartresume/bin/pip install --no-cache-dir -q torch==2.4.1 "transformers>=4.53,<5.0.0" "huggingface-hub>=0.30.0" fastapi "uvicorn[standard]" numpy==1.26.4
echo "[3/5] download model from HuggingFace"
mkdir -p /opt/smartresume/model
/opt/smartresume/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('Alibaba-EI/SmartResume', allow_patterns='Qwen3-0.6B/*', local_dir='/opt/smartresume/hf', local_dir_use_symlinks=False)" && cp -r /opt/smartresume/hf/Qwen3-0.6B/. /opt/smartresume/model/
echo "[4/5] write app.py"
mkdir -p /opt/smartresume/app
cat > /opt/smartresume/app/app.py <<'PYEOF'
{app_py}
PYEOF
echo "[5/5] start server"
cd /opt/smartresume/app
nohup /opt/smartresume/bin/uvicorn app:app --host 0.0.0.0 --port 8000 >> /var/log/fipilot_server.log 2>&1 &
echo "SETUP_DONE"
"""

template = {
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources": [
        {
            "type": "Microsoft.Network/publicIPAddresses",
            "apiVersion": "2023-09-01",
            "name": f"{VM_NAME}-pip",
            "location": LOCATION,
            "sku": {"name": "Standard"},
            "properties": {
                "publicIPAllocationMethod": "Static",
                "dnsSettings": {"domainNameLabel": DNS_LABEL},
            },
        },
        {
            "type": "Microsoft.Network/networkSecurityGroups",
            "apiVersion": "2023-09-01",
            "name": f"{VM_NAME}-nsg",
            "location": LOCATION,
            "properties": {
                "securityRules": [
                    {"name": "ssh", "properties": {"access": "Allow", "direction": "Inbound",
                        "protocol": "Tcp", "priority": 1000, "sourcePortRange": "*",
                        "destinationPortRange": "22", "sourceAddressPrefix": "*", "destinationAddressPrefix": "*"}},
                    {"name": "api", "properties": {"access": "Allow", "direction": "Inbound",
                        "protocol": "Tcp", "priority": 1001, "sourcePortRange": "*",
                        "destinationPortRange": "8000", "sourceAddressPrefix": "*", "destinationAddressPrefix": "*"}},
                ]
            },
        },
        {
            "type": "Microsoft.Network/virtualNetworks",
            "apiVersion": "2023-09-01",
            "name": f"{VM_NAME}-vnet",
            "location": LOCATION,
            "properties": {
                "addressSpace": {"addressPrefixes": ["10.10.0.0/16"]},
                "subnets": [{"name": "default", "properties": {"addressPrefix": "10.10.0.0/24",
                    "networkSecurityGroup": {"id": f"[resourceId('Microsoft.Network/networkSecurityGroups', '{VM_NAME}-nsg')]"}}}],
            },
        },
        {
            "type": "Microsoft.Network/networkInterfaces",
            "apiVersion": "2023-09-01",
            "name": f"{VM_NAME}-nic",
            "location": LOCATION,
            "dependsOn": [f"{VM_NAME}-pip", f"{VM_NAME}-vnet"],
            "properties": {
                "ipConfigurations": [{
                    "name": "ipconfig1",
                    "properties": {
                        "subnet": {"id": f"[resourceId('Microsoft.Network/virtualNetworks/subnets', '{VM_NAME}-vnet', 'default')]"},
                        "publicIPAddress": {"id": f"[resourceId('Microsoft.Network/publicIPAddresses', '{VM_NAME}-pip')]"},
                    },
                }],
            },
        },
        {
            "type": "Microsoft.Compute/virtualMachines",
            "apiVersion": "2023-09-01",
            "name": VM_NAME,
            "location": LOCATION,
            "dependsOn": [f"{VM_NAME}-nic"],
            "properties": {
                "hardwareProfile": {"vmSize": "Standard_NC4as_T4_v3"},
                "osProfile": {
                    "computerName": VM_NAME,
                    "adminUsername": "azureuser",
                    "linuxConfiguration": {"disablePasswordAuthentication": True,
                        "ssh": {"publicKeys": [{"path": "/home/azureuser/.ssh/authorized_keys",
                            "keyData": pub_key}]}},
                },
                "storageProfile": {
                    "imageReference": {"publisher": "microsoft-dsvm", "offer": "ubuntu-2204",
                        "sku": "2204-gen2", "version": "latest"},
                    "osDisk": {"createOption": "FromImage", "managedDisk": {"storageAccountType": "StandardSSD_LRS"},
                        "diskSizeGB": 80},
                },
                "networkProfile": {"networkInterfaces": [
                    {"id": f"[resourceId('Microsoft.Network/networkInterfaces', '{VM_NAME}-nic')]"}]},
                "diagnosticsProfile": {"bootDiagnostics": {"enabled": False}},
            },
        },
        {
            "type": "Microsoft.Compute/virtualMachines/extensions",
            "apiVersion": "2023-09-01",
            "name": f"{VM_NAME}/setup",
            "location": LOCATION,
            "dependsOn": [VM_NAME],
            "properties": {
                "publisher": "Microsoft.Azure.Extensions",
                "type": "CustomScript",
                "typeHandlerVersion": "2.1",
                "autoUpgradeMinorVersion": True,
                "settings": {"commandToExecute": custom_script},
            },
        },
    ],
}

deploy_url = (f"https://management.azure.com/subscriptions/{SUB}/resourceGroups/{RG}/"
              f"providers/Microsoft.Resources/deployments/deploy-gpu-vm?api-version=2022-09-01")
body = json.dumps({"properties": {"mode": "Incremental", "template": template}}).encode()
req = urllib.request.Request(deploy_url, data=body, method="PUT",
                             headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
print("[deploy] creating GPU VM (ARM deployment) ...")
try:
    resp = urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print("DEPLOYMENT FAILED:", e.read().decode()[:2000])
    raise SystemExit(1)

print("=== DEPLOYMENT SUBMITTED ===")
print(f"VM: {VM_NAME}  |  size: Standard_NC4as_T4_v3 (T4 16GB)  |  region: {LOCATION}")
print(f"SSH key: {SSH_KEY}")
print(f"DNS: {DNS_LABEL}.{LOCATION}.cloudapp.azure.com")
print("Setup takes ~10-15 min (DSVM image + torch + model download).")
print("Check progress: azure portal -> fipilot-rg -> fipilot-gpu -> Boot diagnostics.")
