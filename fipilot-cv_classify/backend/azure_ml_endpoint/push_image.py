import json
import subprocess
import sys
import urllib.request
from pathlib import Path

from azure.identity import DeviceCodeCredential

TENANT = "a7d5926e-252e-4db7-864e-195c5dc5f20e"
SUB = "73a4190e-3ee3-43ff-bf0a-40506e4fe7c1"
RG = "fipilot-rg"
ACR_NAME = "fipilotacrizah"
IMAGE_TAG = sys.argv[1] if len(sys.argv) > 1 else "v3-gpu"

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent

cred = DeviceCodeCredential(tenant_id=TENANT)
token = cred.get_token("https://management.azure.com/.default").token

acr_id = f"/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.ContainerRegistry/registries/{ACR_NAME}"
url = f"https://management.azure.com{acr_id}/listCredentials?api-version=2023-07-01"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
creds = json.load(urllib.request.urlopen(req))
username = creds["username"]
password = creds["passwords"][0]["value"]
server = f"{ACR_NAME}.azurecr.io"
image = f"{server}/smartresume:{IMAGE_TAG}"

print(f"[docker] login {server} ...")
subprocess.run(["docker", "login", server, "-u", username, "--password-stdin"],
               input=password.encode(), check=True, cwd=BACKEND_DIR)
print(f"[docker] push {image} ... (this can take 5-15 min)")
subprocess.run(["docker", "push", image], check=True, cwd=BACKEND_DIR)
print("PUSHED:", image)
