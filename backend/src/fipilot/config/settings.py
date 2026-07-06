from dataclasses import dataclass
import os
from pathlib import Path

def _find_root() -> Path:
    path = Path(__file__).resolve()
    while not (path / "pyproject.toml").exists():
        path = path.parent
    return path

ROOT = _find_root()

@dataclass(frozen=True)
class Config:    
    ROOT:           Path = ROOT
    DATA_DIR:       Path = ROOT / "data"
    INPUT_DATA_DIR: Path = ROOT / "data" / "raw" / "resumes"
    OUTPUT_DATA_DIR:Path = ROOT / "data" / "processed" / "resume_image_v2"
    PAGE_IMAGE_DIR: Path = ROOT / "test" / "page_image"
    YOLO_MODEL:     Path = ROOT / "models" / "yolo26_train_results" / "weights" / "best.pt"
    TXT_DIR = Path = ROOT / "data" / "processed" / "resume_text"
    JSON_DIR = Path = ROOT / "data" / "processed" / "resume_json"

    IOA_THRESHOLD: float = 0.85
    LLM_MODEL: str = "llama-3.3-70b-versatile"

    MAX_WORKER: int = 2
    MAX_RETRIES: int = 3

cfg = Config()