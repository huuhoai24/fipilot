import json
import os
from typing import Any, Dict


def init() -> None:
    global model, tokenizer

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_path = os.environ.get("AZUREML_MODEL_DIR", os.getcwd())

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        trust_remote_code=True,
        torch_dtype=torch.float32,
    )
    model.eval()

    if torch.cuda.is_available():
        model = model.to("cuda")
    else:
        model = model.to("cpu")

    print(f"SmartResume model loaded from {model_path}")


def run(raw_data: str) -> Dict[str, Any]:
    import torch

    data = json.loads(raw_data)

    system_prompt = data.get("system_prompt", "")
    user_prompt = data.get("user_prompt", "")
    max_new_tokens = int(data.get("max_new_tokens", 256))
    temperature = float(data.get("temperature", 0.1))

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    text = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )

    return {"text": text}
