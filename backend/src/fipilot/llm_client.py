import json
import logging
import os
import re
import time
from jinja2 import Environment, FileSystemLoader
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from fipilot.config.settings import cfg

logger = logging.getLogger(__name__)
env = Environment(loader=FileSystemLoader(os.path.join(cfg.ROOT, "prompts")))


class LLMClient:
    """LLM client responsible for model initialization, inference, batching, and parsing."""

    def __init__(
        self,
        source_model: str = "Alibaba-EI/SmartResume",
        llm_model: str = "Qwen3-0.6B",
        max_retries: int = 3,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.source_model = source_model
        self.llm_model = llm_model
        self.max_retries = max_retries
        self.device = device

        # Load Tokenizer
        model_id = f"{source_model}/{llm_model}" if not os.path.exists(os.path.join(source_model, llm_model)) else os.path.join(source_model, llm_model)
        if not os.path.exists(model_id) and not "/" in model_id:
            model_id = source_model  # fallback

        self.tokenizer = AutoTokenizer.from_pretrained(source_model, subfolder=llm_model)

        # Try loading vLLM if CUDA is available
        self.use_vllm = False
        self.vllm_model = None

        # Qwen3 is not natively supported by vLLM. Disable vLLM for Qwen3 to avoid weight conflicts.
        is_qwen3 = "qwen3" in llm_model.lower() or "qwen3" in source_model.lower()

        # Khôi phục config.json nếu bị poisoned (từng bị vá thành qwen2/Qwen2ForCausalLM)
        try:
            from huggingface_hub import snapshot_download
            repo_path = snapshot_download(repo_id=source_model)
            model_path = os.path.join(repo_path, llm_model)
            config_file = os.path.join(model_path, "config.json")
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)

                # Nếu config đã bị đổi sang Qwen2, khôi phục lại Qwen3 gốc
                if "architectures" in config_data and "Qwen2ForCausalLM" in config_data["architectures"]:
                    config_data["architectures"] = ["Qwen3ForCausalLM"]
                    config_data["model_type"] = "qwen3"
                    if "rope_scaling" in config_data:
                        config_data["rope_scaling"] = None
                    with open(config_file, "w", encoding="utf-8") as f:
                        json.dump(config_data, f, indent=2)
                    print("🔧 [Heal] Đã tự động khôi phục config.json bị lỗi từ 'qwen2' về 'qwen3'.")
                    logger.info("🔧 [Heal] Restored config.json from qwen2 to qwen3.")
        except Exception as restore_err:
            logger.warning(f"Không thể khôi phục config.json: {restore_err}")

        if torch.cuda.is_available() and not is_qwen3:
            try:
                from vllm import LLM, SamplingParams
                from huggingface_hub import snapshot_download

                repo_path = snapshot_download(repo_id=source_model)
                model_path = os.path.join(repo_path, llm_model)

                # Chỉ patch config.json đối với các model hỗ trợ vLLM (Không phải Qwen3)
                config_file = os.path.join(model_path, "config.json")
                if os.path.exists(config_file):
                    try:
                        with open(config_file, "r", encoding="utf-8") as f:
                            config_data = json.load(f)

                        modified = False
                        if "rope_scaling" not in config_data or config_data["rope_scaling"] is None:
                            config_data["rope_scaling"] = {"type": "linear", "factor": 1.0}
                            modified = True
                            print("🔧 Đã tự động bổ sung rope_scaling cho vLLM.")
                        elif isinstance(config_data["rope_scaling"], dict):
                            if "factor" not in config_data["rope_scaling"]:
                                config_data["rope_scaling"]["factor"] = 1.0
                                modified = True
                                print("🔧 Đã bổ sung rope_scaling.factor cho vLLM.")

                        if modified:
                            with open(config_file, "w", encoding="utf-8") as f:
                                json.dump(config_data, f, indent=2)
                    except Exception as patch_err:
                        print(f"⚠️ Không thể vá config.json: {patch_err}")

                self.vllm_sampling_params = SamplingParams(
                    temperature=0.1,
                    top_p=0.95,
                    max_tokens=2048,
                    repetition_penalty=1.05
                )
                self.vllm_model = LLM(
                    model=model_path,
                    tokenizer=model_path,
                    trust_remote_code=False,
                    tensor_parallel_size=torch.cuda.device_count() or 1,
                    gpu_memory_utilization=0.9,
                    max_model_len=32768,
                    enforce_eager=False,
                    swap_space=4,
                    dtype="float16"
                )
                self.use_vllm = True
                logger.info("Loaded vLLM for fast GPU inference.")
            except Exception as e:
                import traceback
                print("\n=== vLLM Load Traceback ===")
                traceback.print_exc()
                print("===========================\n")
                self.use_vllm = False
                self.vllm_model = None
                print(f"⚠️ Không thể tải vLLM (Lỗi: {type(e).__name__}: {e}). Đang sử dụng thư viện transformers...")
                logger.warning(f"vLLM load failed: {e}. Falling back to transformers.")

        if not self.use_vllm:
            dtype = torch.float16 if "cuda" in self.device else torch.float32
            self.model = AutoModelForCausalLM.from_pretrained(
                source_model,
                subfolder=llm_model,
                torch_dtype=dtype,
                device_map="auto" if "cuda" in self.device else None,
                trust_remote_code=True
            )
            if "cpu" in self.device:
                self.model = self.model.to(self.device)
            logger.info(f"Loaded transformers model on {self.device} with dtype {dtype}")

    def _parse_json(self, raw: str) -> dict:
        # Xóa block <think>...</think> nếu model tự động sinh ra
        raw_clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)

        raw_clean = raw_clean.strip()
        if raw_clean.startswith("{{"):
            raw_clean = raw_clean[1:]

        match = re.search(r"\{.*\}", raw_clean, re.DOTALL)
        if not match:
            # Thử khôi phục nếu JSON bị thiếu dấu đóng ngoặc nhọn do bị ngắt quãng giữa chừng
            if not raw_clean.endswith("}"):
                raw_clean += "\n}"
            match = re.search(r"\{.*\}", raw_clean, re.DOTALL)
            if not match:
                raise ValueError(f"Không tìm thấy JSON hợp lệ trong output: {raw[:200]}")

        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as decode_err:
            logger.warning(f"Standard JSON parsing failed: {decode_err}. Attempting auto-repair...")
            # Sửa các lỗi cú pháp JSON cơ bản
            repaired_str = json_str
            # Thay thế nháy đơn thành nháy kép quanh key/value
            repaired_str = re.sub(r"'(.*?)'", r'"\1"', repaired_str)
            # Sửa boolean/None của Python
            repaired_str = re.sub(r"\bTrue\b", "true", repaired_str)
            repaired_str = re.sub(r"\bFalse\b", "false", repaired_str)
            repaired_str = re.sub(r"\bNone\b", "null", repaired_str)
            # Xóa dấu phẩy thừa ở cuối các phần tử JSON (trailing commas)
            repaired_str = re.sub(r",\s*([\]}])", r"\1", repaired_str)

            try:
                return json.loads(repaired_str)
            except Exception:
                # Fallback to json_repair if available
                try:
                    import json_repair
                    return json_repair.loads(json_str)
                except ImportError:
                    pass
                raise decode_err

    def llm_classify(self, prompt_template: str, resume: str, attempt: int = 0) -> dict:
        template = env.get_template(prompt_template)
        prompt = template.render(resume_text=resume)

        messages = [
            {
                "role": "system",
                "content": "You are a professional resume analysis assistant, your task is to convert the given resume text into the following JSON output."
            },
            {"role": "user", "content": prompt}
        ]

        # Apply chat template correctly (disabling thinking mode if supported)
        try:
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True,
                chat_template_kwargs={"enable_thinking": False}
            )
        except Exception:
            # Fallback if chat_template_kwargs is not supported
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )

        # Force JSON response by pre-filling the assistant output with "{"
        # This completely skips reasoning/thinking blocks (<think>) and forces direct JSON generation.
        formatted_prompt = formatted_prompt.strip()
        if formatted_prompt.endswith("assistant"):
            formatted_prompt += "\n{"
        else:
            formatted_prompt += " {"

        # Dynamic parameter adjustments based on template and attempt index
        is_combined = prompt_template == "combined.jinja2"
        max_tokens = 4096 if is_combined else 2048

        if self.use_vllm:
            # Create a copy or new instance of SamplingParams to customize max_tokens and temperature
            from vllm import SamplingParams
            sampling_params = SamplingParams(
                temperature=1.0 if attempt > 0 else 0.1,
                top_p=0.95,
                max_tokens=max_tokens,
                repetition_penalty=1.05
            )
            outputs = self.vllm_model.generate([formatted_prompt], sampling_params, use_tqdm=False)
            raw = "{" + outputs[0].outputs[0].text
        else:
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=32768
            )

            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}

            gen_kwargs = {
                "max_new_tokens": max_tokens,
                "repetition_penalty": 1.1,
                "pad_token_id": self.tokenizer.eos_token_id,
                "eos_token_id": self.tokenizer.eos_token_id
            }
            if attempt > 0:
                gen_kwargs["do_sample"] = True
                gen_kwargs["temperature"] = 1.0
            else:
                gen_kwargs["do_sample"] = False

            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    **gen_kwargs
                )

            input_len = inputs['input_ids'].shape[1]
            raw = "{" + self.tokenizer.decode(out[0][input_len:], skip_special_tokens=True)

        # Cleanup JSON output
        raw = raw.strip().replace('\\"', '"')
        if raw.startswith("{{"):
            raw = raw[1:]
        return self._parse_json(raw)

    def extract_all(self, resume_text: str, TEMPLATES: list[str], KEYS: list[str]) -> dict:
        # Check if we should use Hugging Face batch inference (on CUDA) or sequential fallback
        use_hf_batching = "cuda" in self.device and not self.use_vllm and len(TEMPLATES) > 1

        # 1. OPTIMIZATION: Hugging Face GPU Batch Inference (Parallel generation on GPU)
        if use_hf_batching:
            try:
                print(f"  🤖 [HF GPU Batching] Đang trích xuất song song {len(TEMPLATES)} phần bằng batch inference...", flush=True)
                start_section = time.time()

                formatted_prompts = []
                for tmpl in TEMPLATES:
                    template = env.get_template(tmpl)
                    prompt = template.render(resume_text=resume_text)
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a professional resume analysis assistant, your task is to convert the given resume text into the following JSON output."
                        },
                        {"role": "user", "content": prompt}
                    ]
                    try:
                        formatted = self.tokenizer.apply_chat_template(
                            messages, tokenize=False, add_generation_prompt=True,
                            chat_template_kwargs={"enable_thinking": False}
                        )
                    except Exception:
                        formatted = self.tokenizer.apply_chat_template(
                            messages, tokenize=False, add_generation_prompt=True
                        )

                    # Force JSON response by pre-filling the assistant output with "{"
                    formatted = formatted.strip()
                    if formatted.endswith("assistant"):
                        formatted += "\n{"
                    else:
                        formatted += " {"
                    formatted_prompts.append(formatted)

                # Set padding token if not set
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                # Left padding is required for batched generation in causal LMs
                self.tokenizer.padding_side = "left"

                inputs = self.tokenizer(
                    formatted_prompts,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=32768
                )

                device = next(self.model.parameters()).device
                inputs = {k: v.to(device) for k, v in inputs.items()}

                with torch.no_grad():
                    out = self.model.generate(
                        **inputs,
                        max_new_tokens=2048,
                        do_sample=False,
                        repetition_penalty=1.1,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )

                input_len = inputs['input_ids'].shape[1]

                results = {}
                for i, key in enumerate(KEYS):
                    generated_tokens = out[i][input_len:]
                    raw = "{" + self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
                    raw = raw.strip().replace('\\"', '"')
                    if raw.startswith("{{"):
                        raw = raw[1:]
                    results[key] = self._parse_json(raw)

                print(f"  ✅ Hoàn thành Batching GPU trong {time.time() - start_section:.2f} giây.", flush=True)
                return results
            except Exception as e:
                logger.error(f"HF GPU Batch inference failed: {e}. Falling back to sequential execution...")
                print(f"  ⚠️ HF GPU Batch thất bại: {e}. Đang chuyển sang chạy tuần tự...", flush=True)

        # 2. OPTIMIZATION: vLLM Batch Inference (if use_vllm is True and multiple templates exist)
        if self.use_vllm and len(TEMPLATES) > 1:
            try:
                print(f"  🤖 [vLLM Batch] Đang trích xuất song song {len(TEMPLATES)} phần...", flush=True)
                start_section = time.time()

                formatted_prompts = []
                for tmpl in TEMPLATES:
                    template = env.get_template(tmpl)
                    prompt = template.render(resume_text=resume_text)
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a professional resume analysis assistant, your task is to convert the given resume text into the following JSON output."
                        },
                        {"role": "user", "content": prompt}
                    ]
                    try:
                        formatted = self.tokenizer.apply_chat_template(
                            messages, tokenize=False, add_generation_prompt=True,
                            chat_template_kwargs={"enable_thinking": False}
                        )
                    except Exception:
                        formatted = self.tokenizer.apply_chat_template(
                            messages, tokenize=False, add_generation_prompt=True
                        )

                    formatted = formatted.strip()
                    if formatted.endswith("assistant"):
                        formatted += "\n{"
                    else:
                        formatted += " {"
                    formatted_prompts.append(formatted)

                # Generate outputs in a single batch call
                outputs = self.vllm_model.generate(formatted_prompts, self.vllm_sampling_params, use_tqdm=False)

                results = {}
                for i, key in enumerate(KEYS):
                    raw = "{" + outputs[i].outputs[0].text
                    raw = raw.strip().replace('\\"', '"')
                    if raw.startswith("{{"):
                        raw = raw[1:]
                    results[key] = self._parse_json(raw)

                print(f"  ✅ Hoàn thành Batching vLLM trong {time.time() - start_section:.2f} giây.", flush=True)
                return results
            except Exception as e:
                logger.error(f"vLLM Batch inference failed: {e}. Falling back to sequential execution...")
                print(f"  ⚠️ vLLM Batch thất bại: {e}. Đang chuyển sang chạy tuần tự...", flush=True)

        # 3. Fallback: Sequential Extraction
        results = [None] * len(TEMPLATES)
        errors = {}

        for i, tmpl in enumerate(TEMPLATES):
            last_err = None
            for attempt in range(self.max_retries):
                try:
                    if attempt == 0:
                        print(f"  🤖 [{i+1}/{len(TEMPLATES)}] Đang trích xuất phần '{KEYS[i]}'...", flush=True)
                    else:
                        print(f"  🔄 Thử lại lần {attempt}/{self.max_retries-1} cho '{KEYS[i]}'...", flush=True)

                    start_section = time.time()
                    results[i] = self.llm_classify(tmpl, resume_text, attempt=attempt)
                    print(f"  ✅ Hoàn thành '{KEYS[i]}' trong {time.time() - start_section:.2f} giây.", flush=True)
                    break
                except Exception as e:
                    last_err = e
                    if attempt < self.max_retries - 1:
                        time.sleep(1)
            else:
                errors[KEYS[i]] = str(last_err)
                logger.error(f"Section '{KEYS[i]}' failed permanently: {last_err}")

        if errors:
            logger.warning(f"extract_all completed with {len(errors)} failed sections: {list(errors.keys())}")

        return {key: results[i] for i, key in enumerate(KEYS) if results[i] is not None}
