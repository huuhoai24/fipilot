from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Config:
    hf_token: str= os.environ["HF_TOKEN"] 
    


cfg = Config()