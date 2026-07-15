import json
import logging
import os
import re
import shutil
import tempfile
import threading
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from ultralytics import YOLO

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from fipilot.config.settings import cfg
from fipilot.utils.resume_extract_module import get_area, get_ioa, is_center_inside, clean_text
from fipilot.utils.resume_extract_module import enrich_output, save_resume_data, is_scanned_pdf

load_dotenv()

# Set HF_TOKEN if available in .env to suppress warnings and speed up downloads
if os.getenv("HUGGINGFACE_API_KEY"):
    os.environ["HF_TOKEN"] = os.getenv("HUGGINGFACE_API_KEY")

env = Environment(loader=FileSystemLoader(os.path.join(cfg.ROOT, "prompts")))
logger = logging.getLogger(__name__)

class ResumeExtract:
    def __init__(
        self,
        yolo_model: str,
        source_model: str = "Alibaba-EI/SmartResume",
        llm_model: str = "Qwen3-0.6B",
        dpi: int = 200,
        max_workers: int = 1,
        max_retries: int = 3,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.yolo_model = YOLO(yolo_model)
        self.dpi = dpi
        self.llm_model = llm_model
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.source_model = source_model
        self.device = device
        
        # Load Tokenizer
        model_id = f"{source_model}/{llm_model}" if not os.path.exists(os.path.join(source_model, llm_model)) else os.path.join(source_model, llm_model)
        if not os.path.exists(model_id) and not "/" in model_id:
            model_id = source_model # fallback
            
        self.tokenizer = AutoTokenizer.from_pretrained(source_model, subfolder=llm_model)
        
        # Try loading vLLM if CUDA is available
        self.use_vllm = False
        self.vllm_model = None
        
        if torch.cuda.is_available():
            try:
                from vllm import LLM, SamplingParams
                from huggingface_hub import snapshot_download
                
                # Tải repo từ HF và xác định đường dẫn thư mục chứa model
                repo_path = snapshot_download(repo_id=source_model)
                model_path = os.path.join(repo_path, llm_model)
                
                # Patch config.json để tránh lỗi RoPE scaling của vLLM
                config_file = os.path.join(model_path, "config.json")
                if os.path.exists(config_file):
                    try:
                        with open(config_file, "r", encoding="utf-8") as f:
                            config_data = json.load(f)
                        
                        modified = False
                        if "rope_scaling" not in config_data or config_data["rope_scaling"] is None:
                            config_data["rope_scaling"] = {"type": "linear", "factor": 1.0}
                            modified = True
                            print("🔧 Đã tự động vá lỗi config.json (bổ sung rope_scaling = {'type': 'linear', 'factor': 1.0}) cho vLLM.")
                        elif isinstance(config_data["rope_scaling"], dict):
                            if "factor" not in config_data["rope_scaling"]:
                                config_data["rope_scaling"]["factor"] = 1.0
                                modified = True
                                print("🔧 Đã tự động vá lỗi config.json (bổ sung rope_scaling.factor = 1.0) cho vLLM.")
                        
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
                    trust_remote_code=True,
                    tensor_parallel_size=torch.cuda.device_count() or 1,
                    gpu_memory_utilization=0.9,
                    max_model_len=32768,
                    enforce_eager=False,
                    swap_space=4
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
                source_model, subfolder=llm_model,
                torch_dtype=dtype,
                device_map="auto" if "cuda" in self.device else None
            )
            if "cpu" in self.device:
                self.model = self.model.to(self.device)
            logger.info(f"Loaded transformers model on {self.device} with dtype {dtype}")

    # saved image into location    
    def pdf_to_images(self, pdf_path: str, output_dir: str, overwrite: bool = False) -> list[Path]:  
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not exists: {pdf_path}")
        
        output = Path(output_dir)
        if not output.exists():
            output.mkdir(parents=True, exist_ok=True)

        file_paths = []
        with pymupdf.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=self.dpi)
                out_path = output / f"{Path(pdf_path).stem}_page_{page_num+1}.png"
                pix.save(str(out_path))
                file_paths.append(out_path)
        return file_paths

    # saved image into tempfile   
    @contextmanager
    def pdf_to_images_tmp(self, pdf_path: str | Path):
        with tempfile.TemporaryDirectory() as tmp:
            yield self.pdf_to_images(pdf_path, tmp, overwrite=True)
    
    def layout_detection(self, pdf_path: str | Path, batch_size: int = 8) -> dict:
        all_detection = {}
        with self.pdf_to_images_tmp(pdf_path) as images:
            results = self.yolo_model(images, batch=batch_size, imgsz=640, stream=True, verbose=False)
            for image, result in zip(images, results):
                all_detection[Path(image).name] = result.boxes.xyxy.cpu().numpy().tolist()
        return all_detection
    
    @staticmethod
    def remove_duplicate_boxes(yolo_boxes: dict, ioa_threshold: float = 0.85) -> dict:
        all_boxes = {}
        for image, boxes in yolo_boxes.items():
            n = len(boxes)
            areas = [get_area(b) for b in boxes]
            boxes_remove = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if i in boxes_remove or j in boxes_remove:
                        continue
                    if areas[i] <= areas[j]:
                        smaller, larger = i, j
                    else:
                        smaller, larger = j, i
                    ioa = get_ioa(boxes[smaller], boxes[larger])
                    if ioa >= ioa_threshold:
                        boxes_remove.add(smaller)
            all_boxes[image] = [boxes[k] for k in range(n) if k not in boxes_remove]
        return all_boxes

    # pairse resume 
    def pair_resume(self, pdf_path: str):
        scale = self.dpi / 72
        results_by_page = {}
        with pymupdf.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_dict = page.get_text("dict")
                page_lines = []
                for block in page_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            x0, y0, x1, y1 = line["bbox"]
                            scaled_bbox = (x0 * scale, y0 * scale, x1 * scale, y1 * scale)
                            raw_text = "".join(span.get("text", "") for span in line.get("spans", []))
                            normalized_text = clean_text(raw_text)
                            if normalized_text:
                                page_lines.append({"bbox": scaled_bbox, "text": normalized_text})
                results_by_page[f"{Path(pdf_path).stem}_page_{page_num + 1}.png"] = page_lines
        return results_by_page

    @staticmethod
    def inter_segment_sorting(all_boxes, page_height=None, y_tolerance=50):
        if page_height is not None:
            y_tolerance = int(page_height * 0.08)
        final_boxes = {}
        for image, boxes in all_boxes.items():
            if not boxes:
                final_boxes[image] = []
                continue
            sorted_by_y = sorted(boxes, key=lambda x: x[1])
            rows = []
            current_row = [sorted_by_y[0]]
            for box in sorted_by_y[1:]:
                if abs(box[1] - current_row[0][1]) <= y_tolerance:
                    current_row.append(box)
                else:
                    rows.append(current_row)
                    current_row = [box]
            rows.append(current_row)

            final_sorted_row = []
            for row in rows:
                sorted_row = sorted(row, key=lambda box: box[0])
                final_sorted_row.extend(sorted_row)
            final_boxes[image] = final_sorted_row

        return final_boxes
    
    @staticmethod
    def intra_segment_sorting(inter_seg_box, resume_lines):
        layout_regions = [
            {"image": image, "bbox": bbox, "contained_blocks": []}
            for image, boxes in inter_seg_box.items()
            for bbox in boxes
        ]

        regions_by_image = {}
        for region in layout_regions:
            regions_by_image.setdefault(region["image"], []).append(region)

        for image, page_lines in resume_lines.items():
            candidate_regions = regions_by_image.get(image, [])
            for line in page_lines:
                best_region = None
                best_score = 0.0
                for region in candidate_regions:
                    if is_center_inside(line["bbox"], region["bbox"]):
                        score = get_ioa(line["bbox"], region["bbox"])
                        if score > best_score:
                            best_score = score
                            best_region = region
                if best_region is not None:
                    best_region["contained_blocks"].append(line)

        for region in layout_regions:
            region["contained_blocks"].sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))

        return layout_regions

    @staticmethod
    def linearize_layout_regions(layout_regions):
        linearized_lines = []
        line_index = 0
        for region in layout_regions:
            for block in region["contained_blocks"]:
                text = block["text"].strip()
                if text:
                    linearized_lines.append(f"[{line_index}]: {text}")
                    line_index += 1
        linearized_text = "\n".join(linearized_lines)
        return linearized_text

    def _parse_json(self, raw: str) -> dict:
        # Xóa block <think>...</think> nếu model tự động sinh ra
        raw_clean = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL)
        
        match = re.search(r"\{.*\}", raw_clean, re.DOTALL)
        if not match:
            raise ValueError(f"Không tìm thấy JSON hợp lệ trong output: {raw[:200]}")
        return json.loads(match.group(0))

    # llm extraction using local model
    def llm_classify(self, prompt_template: str, resume: str) -> dict:
        template = env.get_template(prompt_template)
        prompt = template.render(resume_text=resume)

        messages = [
            {"role": "system", "content": "You are a professional resume analysis assistant, your task is to convert the given resume text into the following JSON output."},
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

        last_err = None
        for attempt in range(self.max_retries):
            try:
                if self.use_vllm:
                    outputs = self.vllm_model.generate([formatted_prompt], self.vllm_sampling_params, use_tqdm=False)
                    raw = outputs[0].outputs[0].text
                else:
                    inputs = self.tokenizer(
                        formatted_prompt,
                        return_tensors="pt",
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
                            pad_token_id=self.tokenizer.eos_token_id,
                            eos_token_id=self.tokenizer.eos_token_id
                        )
                    
                    input_len = inputs['input_ids'].shape[1]
                    raw = self.tokenizer.decode(out[0][input_len:], skip_special_tokens=True)
                
                # Cleanup JSON output
                raw = raw.strip().replace('\\"', '"')
                return self._parse_json(raw)
                
            except Exception as e:
                last_err = e
                logger.warning(f"[{prompt_template}] attempt {attempt+1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1) # Reduced sleep time
                    
        raise RuntimeError(f"llm_classify failed for {prompt_template} after {self.max_retries} attempts") from last_err

    # paralled/sequential extraction
    def extract_all(self, resume_text: str, TEMPLATES: list[str], KEYS: list[str]) -> dict:
        results = [None] * len(TEMPLATES)
        errors = {}

        # Chạy tuần tự để tránh lỗi OOM GPU/tranh chấp CUDA core khi gọi sinh cục bộ
        for i, tmpl in enumerate(TEMPLATES):
            try:
                print(f"  🤖 [{i+1}/{len(TEMPLATES)}] Đang trích xuất phần '{KEYS[i]}'...", flush=True)
                start_section = time.time()
                results[i] = self.llm_classify(tmpl, resume_text)
                print(f"  ✅ Hoàn thành '{KEYS[i]}' trong {time.time() - start_section:.2f} giây.", flush=True)
            except Exception as e:
                errors[KEYS[i]] = str(e)
                logger.error(f"Section '{KEYS[i]}' failed permanently: {e}")

        if errors:
            logger.warning(f"extract_all completed with {len(errors)} failed sections: {list(errors.keys())}")

        return {key: results[i] for i, key in enumerate(KEYS)}
    
    def process_create_data(self, pdf_path, txt_dir, json_dir, TEMPLATES, KEYS, max_retries=5):
        pdf_path = Path(pdf_path)
        if is_scanned_pdf(pdf_path):
            raise ValueError(f"Scanned PDF, no extractable text: {pdf_path}")

        boxes = self.layout_detection(pdf_path)
        boxes = self.remove_duplicate_boxes(boxes)
        boxes = self.inter_segment_sorting(boxes)
        resume_lines = self.pair_resume(pdf_path)
        regions = self.intra_segment_sorting(boxes, resume_lines)
        resume_text = self.linearize_layout_regions(regions)

        # Chuyển đổi txt_dir và json_dir thành Path object trước khi ghi file
        txt_path_dir = Path(txt_dir)
        json_path_dir = Path(json_dir)

        for attempt in range(max_retries):
            try:
                result = self.extract_all(resume_text, TEMPLATES, KEYS)
                break
            except Exception as e:
                # Local execution doesn't have Groq rate limit errors, but keep retry logic for robustness
                logger.warning(f"Extraction failed on {pdf_path}, retry ({attempt+1}/{max_retries}): {e}")
                time.sleep(2 ** attempt)
        else:
            raise RuntimeError(f"Retries exhausted for PDF extraction: {pdf_path}")

        result_add_exp = enrich_output(result)
        return save_resume_data(resume_text, result_add_exp, txt_path_dir, json_path_dir, pdf_path)

    def process_batch(self, pdf_paths, txt_dir, json_dir, TEMPLATES, KEYS):
        results = {}
        total = len(pdf_paths)
        n_success, n_fail = 0, 0

        for i, pdf_path in enumerate(pdf_paths, start=1):
            json_out = Path(json_dir) / f"{Path(pdf_path).stem}.json"
            if json_out.exists():
                logger.info(f"[{i}/{total}] Skip (already exists): {pdf_path}")
                results[str(pdf_path)] = json_out
                n_success += 1
                continue

            logger.info(f"[{i}/{total}] Processing {pdf_path}")
            try:
                results[str(pdf_path)] = self.process_create_data(pdf_path, txt_dir, json_dir, TEMPLATES, KEYS)
                n_success += 1
            except Exception as e:
                logger.error(f"[{i}/{total}] Failed {pdf_path}: {e}")
                results[str(pdf_path)] = {"error": str(e)}
                n_fail += 1

        logger.info(f"Batch done: {n_success} success, {n_fail} failed out of {total}")
        return results