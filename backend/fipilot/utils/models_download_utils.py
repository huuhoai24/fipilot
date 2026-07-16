"""
Model download utilities for SmartResume (Hugging Face source)
"""
import os
from typing import Optional

try:
    from huggingface_hub import snapshot_download as hf_snapshot_download
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False


from .model_paths import ModelPath, ModelType, ModelSource


def auto_download_and_get_model_path(
    relative_path: str,
    model_type: ModelType = ModelType.LLM,
    save_path: Optional[str] = None
) -> str:

    model_source = os.getenv('SMARTRESUME_MODEL_SOURCE', "huggingface")

    if model_source == 'local':
        from .config import config
        local_path = config.model_download.get('models_dir', {}).get(model_type.value, '')
        if not local_path:
            raise ValueError(f"Local path for model_type '{model_type.value}' is not configured.")
        return local_path

    # Repo mapping now points at the Hugging Face repo IDs defined in model_paths.py
    repo_mapping = {
        ModelType.LLM: ModelPath.SMART_RESUME_ROOT_HF.value,
        ModelType.LAYOUT: ModelPath.YOLOV10_ROOT_HF.value,
    }

    if model_type not in repo_mapping:
        raise ValueError(f"Unsupported model_type: {model_type}, must be 'llm' or 'layout'")

    repo = repo_mapping[model_type]

    if not HUGGINGFACE_AVAILABLE:
        raise ImportError("huggingface_hub not available. Install with: pip install huggingface_hub")

    relative_path = relative_path.strip('/')

    download_kwargs = {
        "repo_id": repo,
        "allow_patterns": [relative_path, relative_path + "/*"],
    }

    if save_path:
        os.makedirs(save_path, exist_ok=True)
        download_kwargs["local_dir"] = save_path

    cache_dir = hf_snapshot_download(**download_kwargs)

    if not cache_dir:
        raise FileNotFoundError(f"Failed to download model: {relative_path} from {repo}")

    return cache_dir


def get_model_path(model_type: ModelType) -> Optional[str]:
    from .config import config
    return config.model_download.get('models_dir', {}).get(model_type.value)


def download_model(
    model_type: ModelType,
    model_source: Optional[ModelSource] = None,
    save_path: Optional[str] = None
) -> str:
    if model_source:
        os.environ['SMARTRESUME_MODEL_SOURCE'] = model_source.value

    if model_type == ModelType.LLM:
        return auto_download_and_get_model_path(
            ModelPath.QWEN3_0_6B.value, ModelType.LLM, save_path
        )
    elif model_type == ModelType.LAYOUT:
        return auto_download_and_get_model_path(
            ModelPath.YOLO_MODEL.value, ModelType.LAYOUT, save_path
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


if __name__ == '__main__':
    try:
        llm_path = auto_download_and_get_model_path(
            ModelPath.QWEN3_0_6B.value, ModelType.LLM
        )
        print(f"LLM model path: {llm_path}")

        layout_path = auto_download_and_get_model_path(
            ModelPath.YOLO_MODEL.value, ModelType.LAYOUT
        )
        print(f"Layout model path: {layout_path}")

    except Exception as e:
        print(f"Download failed: {e}")