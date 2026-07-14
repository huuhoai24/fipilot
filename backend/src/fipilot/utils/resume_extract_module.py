import re
from datetime import datetime
import logging
from pathlib import Path
import uuid
import json
import pymupdf

logger = logging.getLogger(__name__)

def get_area(box):
    area = (box[2] - box[0]) * (box[3] - box[1])
    return area

def get_ioa(box_a, box_b):
    ax0, ay0, ax1, ay1 = box_a
    bx0, by0, bx1, by1 = box_b

    inter_x0 = max(ax0, bx0)
    inter_y0 = max(ay0, by0)
    inter_x1 = min(ax1, bx1)
    inter_y1 = min(ay1, by1)

    inter_w = max(0, inter_x1 - inter_x0)
    inter_h = max(0, inter_y1 - inter_y0)
    intersection = inter_w * inter_h

    box_a_area = get_area(box_a)
    
    if box_a_area == 0:
        return 0.0
    ioa = intersection / box_a_area
    return ioa


def is_center_inside(line_bbox, yolo_bbox):
    x0, y0, x1, y1 = line_bbox
    x_center = (x0 + x1) / 2
    y_center = (y0 + y1) / 2

    X_min, Y_min, X_max, Y_max = yolo_bbox
    return (X_min <= x_center <= X_max) and (Y_min <= y_center <= Y_max)

# Nomalize text
def fix_spaced_text(text: str) -> str:
    if not text:
        return ""
    chunks = re.split(r'\s{2,}', text)
    fixed_chunks = []
    for chunk in chunks:
        chunk = chunk.strip()
        chars = chunk.split(' ')
        if len(chars) > 1 and all(len(c) == 1 or c in ['&', '-', '/', '+', ','] for c in chars):
            fixed_chunks.append(''.join(chars))
        else:
            fixed_chunks.append(chunk)
    return ' '.join(fixed_chunks)

def clean_text(text: str) -> str:
    if not text:
        return ""

    # 1. Fix spaced text first before collapsing spaces
    text = fix_spaced_text(text)

    # 2. Normalize bullets (e.g. • to - ) BEFORE filtering, so they are kept
    text = re.sub(r'^[•\u2022➢●■*]\s*', '- ', text)

    # 3. Remove control characters and non-whitelist garbage characters
    # This whitelist is extremely safe and comprehensive, preserving Vietnamese (upper/lower case),
    # numbers, spaces, punctuation, quotes, percent sign, tilde, and programming symbols (+, #, /, @, |, &).
    safe_pattern = r'[^a-zA-Z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸ.,:;?!\(\)\[\]\-–—+#/@|&_%\'"~→=<>]'
    text = re.sub(safe_pattern, '', text)
    
    # 4. Collapse consecutive spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# caulate YOE
def _to_month_idx(date_str: str | None) -> int | None:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m")
    except ValueError:
        return None
    return dt.year * 12 + (dt.month - 1)


def calculate_experience(work_experience: list[dict]) -> dict:
    """
    Tổng kinh nghiệm = union các khoảng thời gian làm việc (interval merge),
    không phải cộng dồn thô -- tránh đếm trùng khi có job overlap.
    Output chỉ gồm years/months, không kèm diagnostic.
    """
    now_idx = datetime.now().year * 12 + (datetime.now().month - 1)

    # Các giá trị coi là "đang làm việc" (chưa kết thúc)
    ONGOING_VALUES = {None, "", "present", "current", "now", "ongoing"}

    intervals = []
    for entry in work_experience:
        start_idx = _to_month_idx(entry.get("startDate"))
        if start_idx is None:
            continue

        end_str = entry.get("endDate")
        normalized_end = end_str.strip().lower() if isinstance(end_str, str) else end_str

        if normalized_end in ONGOING_VALUES:
            end_idx = now_idx
        else:
            end_idx = _to_month_idx(end_str)

        if end_idx is None or end_idx < start_idx:
            continue

        intervals.append((start_idx, end_idx))

    if not intervals:
        return {"total_years": 0, "total_months": 0}

    intervals.sort()
    merged_start, merged_end = intervals[0]
    total = 0
    for start, end in intervals[1:]:
        if start <= merged_end + 1:
            merged_end = max(merged_end, end)
        else:
            total += merged_end - merged_start + 1
            merged_start, merged_end = start, end
    total += merged_end - merged_start + 1

    years, months = divmod(total, 12)
    return {"total_years": years, "total_months": months}


def enrich_output(parsed: dict) -> dict:
    matching = {**parsed["match_info"]["matching"]}
    matching["years_of_experience"] = calculate_experience(
        parsed.get("work_exp", {}).get("workExperience", [])
    )
    return {**parsed, "match_info": {**parsed["match_info"], "matching": matching}}

def atomic_write_text(path: Path, content: str) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp_path.write_text(content, encoding="utf-8")
        tmp_path.replace(path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise

def save_resume_data(resume_text: str, output: dict, txt_dir: str, json_dir: str, pdf_path: str | Path) -> tuple[str, str]:
        base_name = Path(pdf_path).stem
        base_name = "".join(c for c in base_name if c.isalnum() or c in "-_")
        if not base_name:
            base_name = f"resume_{uuid.uuid4().hex[:8]}"

        txt_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        txt_path = txt_dir / f"{base_name}.txt"
        json_path = json_dir / f"{base_name}.json"

        try:
            atomic_write_text(txt_path, resume_text)
            atomic_write_text(json_path, json.dumps(output, ensure_ascii=False, indent=2, default=str))
        except Exception as e:
            logger.error(f"Failed saving resume data for {pdf_path}: {e}")
            txt_path.unlink(missing_ok=True)
            raise

        logger.info(f"Saved TXT: {txt_path}")
        logger.info(f"Saved JSON: {json_path}")
        return str(txt_path), str(json_path)

def is_scanned_pdf(pdf_path: str | Path, text_threshold: int = 20) -> bool:
    with pymupdf.open(pdf_path) as doc:
        total_text = "".join(page.get_text() for page in doc)
    return len(total_text.strip()) < text_threshold