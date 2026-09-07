from pathlib import Path
from pypdf import PdfReader

RAW_DIR = Path(__file__).resolve().parents[1] / "DATA" / "RAW"

for pdf_path in RAW_DIR.glob("*.pdf"):
    print("\n" + "=" * 80)
    print(f"FILE: {pdf_path.name}")

    reader = PdfReader(pdf_path)

    print(f"PAGES: {len(reader.pages)}")

    for page_num, page in enumerate(reader.pages[:3], start=1):
        text = page.extract_text() or ""

        print(f"\n--- PAGE {page_num} ---")
        print(text[:1500])