import json
import os
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor
from fipilot.utils.config import config
from fipilot.utils.prompts import get_prompts

import random
import json_repair

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch



class LLMClient:
    def __init__(self):
        self.prompts = get_prompts()
        self.direct_model = None  
        self.direct_tokenizer = None  
        self._init_direct_model()
    
    def _init_direct_model(self) -> None:
        """Initialize direct model loading"""
        try:
            direct_model_name = getattr(config, 'direct_model_name', None)
            if not direct_model_name:
                print("Warning: direct_model_name is not configured")
                return

            # Try to find model in local models directory first
            local_model_path = None
            models_dir = getattr(config, 'model_download', {}).get('models_dir', {}).get('llm', 'models')

            # Check if it's already a local path
            if os.path.exists(direct_model_name):
                local_model_path = direct_model_name
            else:
                # Try to find in models directory
                possible_paths = [
                    os.path.join(models_dir, direct_model_name),
                    os.path.join(models_dir, os.path.basename(direct_model_name)),
                    os.path.join('models', direct_model_name),
                    os.path.join('models', os.path.basename(direct_model_name))
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        local_model_path = path
                        break

            # If local model not found, try to download it
            if not local_model_path:
                print(f"Local model not found, attempting to download: {direct_model_name}")
                try:
                    from ..utils.models_download_utils import download_model
                    from ..utils.model_paths import ModelType, ModelSource
                    download_model(ModelType.LLM, ModelSource.MODELSCOPE, models_dir)
                    # Try to find the downloaded model
                    for path in possible_paths:
                        if os.path.exists(path):
                            local_model_path = path
                            break
                except Exception as download_error:
                    print(f"Failed to download model: {download_error}")
                    # Fall back to using the original model name (might be from HuggingFace)
                    local_model_path = direct_model_name

            print(f"Loading direct model from: {local_model_path}")

            # Load tokenizer
            self.direct_tokenizer = AutoTokenizer.from_pretrained(
                local_model_path,
                trust_remote_code=True
            )

            # Load model
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.direct_model = AutoModelForCausalLM.from_pretrained(
                local_model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )

            if device == "cpu":
                self.direct_model = self.direct_model.to(device)

            print(f"Direct model loaded successfully on {device}")

        except Exception as e:
            print(f"Failed to load direct model: {e}")
            self.direct_model = None
            self.direct_tokenizer = None

    def extract_info(self, text_content: str, extract_types: List[str], resume_id: str, use_backup_channel: bool = False) -> Dict[str, Any]:
        if not self.direct_model or not self.direct_tokenizer:
            raise RuntimeError(
                "Direct model not loaded. Check 'direct_model_name' in config.yaml "
                "and ensure transformers/torch are installed."
            )
 
        def call_direct_llm(prompt_key: str) -> Dict[str, Any]:
            try:
                system_prompt = self.prompts[prompt_key]
                user_prompt = text_content
 
                if hasattr(self.direct_tokenizer, 'chat_template') and self.direct_tokenizer.chat_template:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                    prompt = self.direct_tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                else:
                    prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
 
                inputs = self.direct_tokenizer(
                    prompt,
                    return_tensors="pt",
                    truncation=True,
                    max_length=4096
                )
 
                device = next(self.direct_model.parameters()).device
                inputs = {k: v.to(device) for k, v in inputs.items()}
 
                with torch.no_grad():
                    outputs = self.direct_model.generate(
                        **inputs,
                        max_new_tokens=1024,
                        temperature=0.1,
                        do_sample=True,
                        pad_token_id=self.direct_tokenizer.eos_token_id,
                        eos_token_id=self.direct_tokenizer.eos_token_id
                    )
 
                response = self.direct_tokenizer.decode(
                    outputs[0][inputs['input_ids'].shape[1]:],
                    skip_special_tokens=True
                )
 
                response = response.strip().replace('\\"', '"')
 
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
 
                if json_start != -1 and json_end > json_start:
                    json_content = response[json_start:json_end]
                    try:
                        return json.loads(json_content)
                    except json.JSONDecodeError:
                        json_content = json_content.replace("'", '"')
                        json_content = json_content.replace('True', 'true')
                        json_content = json_content.replace('False', 'false')
                        json_content = json_content.replace('None', 'null')
                        return json_repair.loads(json_content)
                else:
                    print(f"No valid JSON found in response for {prompt_key}")
                    return {}
 
            except Exception as e:
                print(f"Error in direct model call for {prompt_key}: {e}")
                os.makedirs("contents", exist_ok=True)
                error_info = {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "prompt_key": prompt_key,
                    "model_name": getattr(config, 'direct_model_name', 'unknown')
                }
                with open(f"contents/{resume_id}_{prompt_key}_direct_error.json", "w", encoding='utf-8') as f:
                    json.dump(error_info, f, ensure_ascii=False, indent=2)
                return {}
 
        combined_result = {}
        for extract_type in extract_types:
            result = call_direct_llm(extract_type)
            combined_result.update(result)
 
        return combined_result

