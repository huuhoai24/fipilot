import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from fipilot.resume_extraction import ResumeExtract


def main() -> None:
    pdf_path = ROOT / "test" / "CV_hoainh.pdf"
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return

    print(f"Extracting {pdf_path.name} with PyMuPDF and Azure OpenAI...")
    started_at = time.perf_counter()
    result_json = ResumeExtract().pipeline(pdf_path)
    print(f"Completed in {time.perf_counter() - started_at:.2f} seconds")
    print(result_json)


if __name__ == "__main__":
    main()
