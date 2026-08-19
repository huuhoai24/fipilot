import os
import yaml
from pathlib import Path

def _find_root() -> Path:
    path = Path(__file__).resolve()
    while not (path / "pyproject.toml").exists():
        path = path.parent
    return path

ROOT = _find_root()
CONFIG_PATH = ROOT / "fipilot" / "configs" / "config.yaml"

class ExtractionConfig:
    def __init__(self, ioa_threshold: float = 0.85):
        self.ioa_threshold = ioa_threshold

    def update(self, data: dict):
        if not data:
            return
        for k, v in data.items():
            setattr(self, k, v)

class Config:
    def __init__(self):
        # Set default values
        self.azure_openai = None
        self.yolo_model_name = "best.pt"
        self.model_download = {
            "models_dir": {
                "llm": str(ROOT / "models"),
                "layout": str(ROOT / "models")
            }
        }
        self.extraction = ExtractionConfig()
        
        # Load from config.yaml if it exists
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    yaml_config = yaml.safe_load(f)
                if yaml_config:
                    for k, v in yaml_config.items():
                        if k == "extraction" and isinstance(v, dict):
                            self.extraction.update(v)
                        else:
                            setattr(self, k, v)
            except Exception as e:
                print(f"Error loading config.yaml: {e}")
        
        # Resolve direct_model_name to absolute path if it points to a local directory
        if getattr(self, 'direct_model_name', None):
            if os.path.isabs(self.direct_model_name) and os.path.exists(self.direct_model_name):
                pass
            else:
                possible_paths = [
                    ROOT / "models" / self.direct_model_name,
                    ROOT / "SmartResume_hungingface" / self.direct_model_name,
                    ROOT / self.direct_model_name
                ]
                for p in possible_paths:
                    if p.exists():
                        self.direct_model_name = str(p)
                        break

config = Config()
