from pathlib import Path
from pypdf import PdfReader
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "DATA" / "RAW"
PROCESSED_DIR = PROJECT_ROOT / "DATA" / "Processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

documents = []

for pdf_path in RAW_DIR.glob("*.pdf"):
    reader = PdfReader(pdf_path)

    print(f"Processing: {pdf_path.name}")

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        # Basic cleanup
        text = text.strip()

        if not text:
            continue

        page_record = {
            "document": pdf_path.name,
            "page": page_number,
            "text": text
        }

        documents.append(page_record)

output_file = PROCESSED_DIR / "pages.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=2, ensure_ascii=False)

print()
print(f"Saved {len(documents)} pages")
print(f"Output: {output_file}")