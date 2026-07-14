import json
import logging
import os
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
from ollama import Client
from jinja2 import Environment, FileSystemLoader
from ultralytics import YOLO
from groq import RateLimitError

from fipilot.config.settings import cfg
from fipilot.utils.resume_extract_module import get_area, get_ioa, is_center_inside, clean_text
from fipilot.utils.resume_extract_module import enrich_output, save_resume_data, is_scanned_pdf

load_dotenv()
env = Environment(loader=FileSystemLoader(os.path.join(cfg.ROOT, "prompts")))
logger = logging.getLogger(__name__)

class ResumeExtract:
    def __init__(
        self,
        yolo_model: str,
        llm_model: str,
        dpi: int,
        max_workers: int,
        max_retries: int,
        
    ):
        self.yolo_model = YOLO(yolo_model)
        self.dpi = dpi
        self.llm_model =  llm_model
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.ollama_client = Client(host="https://pronto-swagger-area.ngrok-free.dev")

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
            # results = self.yolo_model(images, batch=batch_size, stream=True)
            results = self.yolo_model(images, batch=batch_size, imgsz=640, stream=True, verbose=False)
            for image, result in zip(images, results):
                all_detection[Path(image).name] = result.boxes.xyxy.cpu().numpy().tolist()
        return all_detection
    
    @staticmethod
    def remove_duplicate_boxes( yolo_boxes: dict, ioa_threshold: float = 0.85) -> dict:
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

        # Đảo vòng lặp: duyệt theo từng dòng trước, tìm vùng khớp nhất
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
                        score = get_ioa(line["bbox"], region["bbox"])  # diện tích giao / diện tích line
                        if score > best_score:
                            best_score = score
                            best_region = region
                if best_region is not None:
                    best_region["contained_blocks"].append(line)
                # else: dòng không thuộc vùng nào -> xử lý ở cách 3

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
        # linearized_text = "\n".join(linearized_lines)
        linearized_text = " ".join(linearized_lines)
        return linearized_text

    # llm extraction
    def llm_classify(self, prompt_template: str, resume: str) -> dict:
        template = env.get_template(prompt_template)
        prompt = template.render(resume_text=resume)

        last_err = None
        for attempt in range(self.max_retries):
            try:
                response = self.ollama_client.chat(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "You are a professional resume analysis assistant, your task is to convert the given resume text into the following JSON output."},
                        {"role": "user", "content": prompt},
                    ],
                    options={"temperature": 0.0},
                    format="json"
                )
                return json.loads(response.message.content)
            except Exception as e:
                last_err = e
                logger.warning(f"[{prompt_template}] attempt {attempt+1}/{self.max_retries} failed: {e}")
                time.sleep(2 ** attempt)  # backoff: 1s, 2s, 4s
        raise RuntimeError(f"llm_classify failed for {prompt_template} after {self.max_retries} attempts") from last_err

    # paralled extraction
    def extract_all(self, resume_text: str, TEMPLATES: list[str], KEYS: list[str]) -> dict:
        results = [None] * len(TEMPLATES)
        errors = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_idx = {
                executor.submit(self.llm_classify, tmpl, resume_text): i
                for i, tmpl in enumerate(TEMPLATES)
            }
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    errors[KEYS[idx]] = str(e)
                    logger.error(f"Section '{KEYS[idx]}' failed permanently: {e}")

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

        for attempt in range(max_retries):
            try:
                result = self.extract_all(resume_text, TEMPLATES, KEYS)
                break
            except RateLimitError as e:
                wait = getattr(e, "retry_after", None) or (2 ** attempt)
                logger.warning(f"Rate limited on {pdf_path}, retry in {wait}s ({attempt+1}/{max_retries})")
                time.sleep(wait)
        else:
            raise RuntimeError(f"Rate limit retries exhausted: {pdf_path}")

        result_add_exp = enrich_output(result)
        return save_resume_data(resume_text, result_add_exp, txt_dir, json_dir, pdf_path)

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