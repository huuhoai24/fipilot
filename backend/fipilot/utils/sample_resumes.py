import os
import shutil
import random
import argparse
from pathlib import Path

def sample_cvs(raw_dir: Path, processed_dir: Path, target_total: int = 400, seed: int = 42, flat: bool = False):
    """
    Samples CVs from raw_dir subdirectories according to their original distribution ratio
    and copies them to processed_dir.
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    
    # Get all subdirectories
    subdirs = sorted([d for d in raw_dir.iterdir() if d.is_dir()])
    
    # Gather pdf files
    dir_files = {}
    total_files = 0
    for d in subdirs:
        pdfs = sorted(list(d.glob("*.pdf")))
        dir_files[d.name] = pdfs
        total_files += len(pdfs)
        
    if total_files == 0:
        raise ValueError(f"No PDF files found in {raw_dir}")
        
    # Hamilton / Largest Remainder Method
    floors = {}
    remainders = {}
    for name, files in dir_files.items():
        exact_target = (len(files) / total_files) * target_total
        floor_val = int(exact_target)
        floors[name] = floor_val
        remainders[name] = exact_target - floor_val
        
    current_sum = sum(floors.values())
    remaining = target_total - current_sum
    
    sorted_by_remainder = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
    for name, _ in sorted_by_remainder[:remaining]:
        floors[name] += 1
        
    # Sample and copy
    rng = random.Random(seed)
    copied_count = 0
    
    for name, files in dir_files.items():
        target = floors[name]
        sampled = rng.sample(files, target)
        
        if flat:
            dest_dir = processed_dir
        else:
            dest_dir = processed_dir / name
            
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in sampled:
            shutil.copy2(f, dest_dir / f.name)
            copied_count += 1
            
    print(f"Successfully sampled and copied {copied_count} files to {processed_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sample CVs according to distribution ratios.")
    parser.add_argument("--raw-dir", type=str, default="data/raw/resumes", help="Path to raw resumes directory")
    parser.add_argument("--processed-dir", type=str, default="data/processed/yolo", help="Path to processed/yolo directory")
    parser.add_argument("--target", type=int, default=400, help="Total target number of CVs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling")
    parser.add_argument("--flat", action="store_true", help="Copy files directly into processed-dir without subfolders")
    args = parser.parse_args()
    
    sample_cvs(
        raw_dir=Path(args.raw_dir),
        processed_dir=Path(args.processed_dir),
        target_total=args.target,
        seed=args.seed,
        flat=args.flat
    )
