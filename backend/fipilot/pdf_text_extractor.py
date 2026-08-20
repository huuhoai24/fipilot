import argparse
from pathlib import Path

import pymupdf


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract page-ordered text from a PDF for use as LLM context."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file: {path}")

    pages = []
    with pymupdf.open(path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text", sort=True).strip()
            if text:
                pages.append(f"[PAGE {page_number}]\n{text}")

    if not pages:
        raise ValueError(
            "No text layer found in the PDF. The file may require OCR before extraction."
        )

    return "\n\n".join(pages)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF using PyMuPDF for LLM input."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional output .txt file; prints to stdout when omitted",
    )
    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Extracted text written to: {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
