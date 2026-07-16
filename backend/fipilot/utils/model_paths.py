from enum import Enum


class ModelPath(Enum):
    """Model path configurations for different model sources"""

    SMART_RESUME_ROOT_HF = "Alibaba-EI/SmartResume"
    YOLOV10_ROOT_HF = "hoainh204/YoloV12s"

    # Specific model paths
    QWEN3_0_6B = "Qwen3-0.6B"
    YOLO_MODEL = "YoloV12s/best.pt"

    # Model types
    LLM_MODEL = "llm"
    LAYOUT_MODEL = "layout"


class ModelType(Enum):
    """Model types for SmartResume"""
    LLM = "llm"           # Large Language Model for text extraction
    LAYOUT = "layout"     # Layout detection model
    ALL = "all"           # All models


class ModelSource(Enum):
    """Model download sources"""
    HUGGINGFACE = "huggingface"
    LOCAL = "local"