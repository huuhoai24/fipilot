import json
import logging
import os
import re
import tempfile

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from ultralytics import YOLO

from fipilot.model.llm_client import LLMClient
from fipilot.utils.config import config
from fipilot.utils.resume_extract_module import get_area, get_ioa, is_center_inside, clean_text
from fipilot.utils.resume_extract_module import is_scanned_pdf

load_dotenv()

# Set HF_TOKEN if available in .env to suppress warnings and speed up downloads
if os.getenv("HUGGINGFACE_API_KEY"):
    os.environ["HF_TOKEN"] = os.getenv("HUGGINGFACE_API_KEY")

logger = logging.getLogger(__name__)


class ResumeExtract:
    def __init__(
        self,
        yolo_model: str = None,
        dpi: int = 150,
    ):
        # Resolve yolo model path from config if not specified, or if it points to non-existent default 'best.pt'
        if yolo_model is None or yolo_model == "None" or yolo_model == "" or yolo_model == "best.pt":
            yolo_model = None

        if yolo_model is None:
            # Get yolo model path from config
            yolo_model_name = getattr(config, 'yolo_model_name', "best.pt")
            models_dir = config.model_download.get('models_dir', {}).get('layout', 'models')
            os.makedirs(models_dir, exist_ok=True)
            
            # Check if it exists locally in the layout models directory
            possible_path = os.path.join(models_dir, yolo_model_name)
            if os.path.exists(possible_path):
                yolo_model = possible_path
            elif os.path.exists(yolo_model_name):
                yolo_model = yolo_model_name
            else:
                # Auto-download the layout model
                print(f"Local YOLO model not found, attempting to download: {yolo_model_name}")
                try:
                    from fipilot.utils.models_download_utils import download_model
                    from fipilot.utils.model_paths import ModelType, ModelSource
                    
                    downloaded_dir = download_model(ModelType.LAYOUT, ModelSource.HUGGINGFACE, models_dir)
                    downloaded_path = os.path.join(downloaded_dir, yolo_model_name)
                    if os.path.exists(downloaded_path):
                        yolo_model = downloaded_path
                    else:
                        yolo_model = downloaded_dir
                except Exception as e:
                    print(f"Failed to download YOLO model: {e}")
                    print("If the repository 'hoainh204/YoloV12s' is private, please set the HF_TOKEN environment variable.")
                    print(f"Alternatively, you can manually upload your model 'best.pt' to: {os.path.abspath(possible_path)}")
                    # Final fallback to standard path
                    yolo_model = possible_path

        self.yolo_model = YOLO(yolo_model)
        self.dpi = dpi

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
    def remove_duplicate_boxes(yolo_boxes: dict, ioa_threshold: float = None) -> dict:
        if ioa_threshold is None:
            ioa_threshold = config.extraction.ioa_threshold
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
        linearized_text = " ".join(linearized_lines)
        return linearized_text

    def llm_analyzer(self, resume_text, resume_id):
        llm_client = LLMClient()
        extract_types = ["work_experience", "education"]
        result = llm_client.extract_info(
            text_content=resume_text,
            extract_types=extract_types,
            resume_id=resume_id
            )
        
        # Parse resume_text to build a mapping from line index to clean text
        lines_map = {}
        for line in resume_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            match = re.match(r'^\[(\d+)\]:\s*(.*)$', line)
            if match:
                idx = int(match.group(1))
                text = match.group(2)
                lines_map[idx] = text

        # Post-process workExperience: replace index range with actual text
        if "workExperience" in result and isinstance(result["workExperience"], list):
            for entry in result["workExperience"]:
                if isinstance(entry, dict):
                    index_range = entry.get("jobDescription_refer_index_range")
                    if isinstance(index_range, list) and len(index_range) == 2:
                        try:
                            start_idx = int(index_range[0])
                            end_idx = int(index_range[1])
                            extracted_lines = []
                            for idx in range(start_idx, end_idx + 1):
                                if idx in lines_map:
                                    extracted_lines.append(lines_map[idx])
                            job_description_text = "\n".join(extracted_lines)
                            entry["jobDescription"] = job_description_text
                            entry["jobDescription_refer_index_range"] = job_description_text
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error parsing index range {index_range}: {e}")

        return json.dumps(result, indent=2, ensure_ascii=False)
        
    def pipeline(self, pdf_path):
        pdf_path = Path(pdf_path)
        if is_scanned_pdf(pdf_path):
            raise ValueError(f"Scanned PDF, no extractable text: {pdf_path}")

        boxes = self.layout_detection(pdf_path)
        boxes = self.remove_duplicate_boxes(boxes)
        boxes = self.inter_segment_sorting(boxes)
        resume_lines = self.pair_resume(pdf_path)
        regions = self.intra_segment_sorting(boxes, resume_lines)
        resume_text = self.linearize_layout_regions(regions)
        result = self.llm_analyzer(resume_text, pdf_path.stem)
        return result
