from pathlib import Path

import yaml


def _find_root() -> Path:
    path = Path(__file__).resolve()
    while not (path / "pyproject.toml").exists():
        path = path.parent
    return path


ROOT = _find_root()
CONFIG_PATH = ROOT / "fipilot" / "configs" / "config.yaml"


class Config:
    def __init__(self):
        self.azure_openai = None

        if CONFIG_PATH.exists():
            try:
                with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
                    yaml_config = yaml.safe_load(config_file)
                if yaml_config:
                    for key, value in yaml_config.items():
                        setattr(self, key, value)
            except Exception as error:
                print(f"Error loading config.yaml: {error}")


config = Config()
