import json
import os
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor

import json_repair
from dotenv import load_dotenv

from fipilot.utils.config import config
from fipilot.utils.prompts import get_prompts


class LLMClient:
    def __init__(self):
        self.prompts = get_prompts()
        self.remote_client = None
        azure = getattr(config, 'azure_openai', None)
        if azure and azure.get('base_url'):
            from openai import OpenAI
            load_dotenv()
            self.model = azure['model']
            self.remote_client = OpenAI(
                base_url=azure['base_url'],
                api_key=os.environ.get(azure.get('api_key_env', 'AZURE_OPENAI_API_KEY')),
                timeout=60.0,
                max_retries=0,
            )
            print(f"SmartResume: using Azure OpenAI endpoint {azure['base_url']} (model: {self.model})")

    def _call_llm(self, system_prompt: str, user_prompt: str, max_new_tokens: int = 1024) -> str:
        if self.remote_client is None:
            raise RuntimeError(
                "Azure OpenAI not configured. Add 'azure_openai' section in config.yaml"
            )

        response = self.remote_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_new_tokens,
            temperature=0.1,
        )
        return response.choices[0].message.content

    def generate_text(self, system_prompt: str, user_prompt: str, max_new_tokens: int = 1024) -> str:
        return self._call_llm(system_prompt, user_prompt, max_new_tokens)

    def extract_info(self, text_content: str, extract_types: List[str], resume_id: str, use_backup_channel: bool = False) -> Dict[str, Any]:
        if self.remote_client is None:
            raise RuntimeError(
                "No LLM available. Configure 'azure_openai' section in config.yaml."
            )

        def call_direct_llm(prompt_key: str) -> Dict[str, Any]:
            try:
                system_prompt = self.prompts[prompt_key]
                user_prompt = text_content

                response = self._call_llm(system_prompt, user_prompt)
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
                    "model_name": self.model
                }
                with open(f"contents/{resume_id}_{prompt_key}_direct_error.json", "w", encoding='utf-8') as f:
                    json.dump(error_info, f, ensure_ascii=False, indent=2)
                raise RuntimeError(f"Failed to extract {prompt_key}: {e}") from e

        combined_result = {}
        for extract_type in extract_types:
            result = call_direct_llm(extract_type)
            combined_result.update(result)

        return combined_result
