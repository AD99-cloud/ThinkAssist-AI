from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "DATA" / "Processed"

INPUT_FILE = PROCESSED_DIR / "clean_pages.json"
OUTPUT_FILE = PROCESSED_DIR / "chunks.json"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150


def split_text(text: str, chunk_size: int, overlap: int):
    text = re.sub(r"\n+", "\n", text).strip()

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)

all_chunks = []

for page in pages:
    document_name = page["document"]
    page_number = page["page"]
    text = page["text"]

    page_chunks = split_text(
        text=text,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    for chunk_number, chunk_text in enumerate(page_chunks, start=1):

        safe_document_name = (
            document_name
            .replace(".pdf", "")
            .replace(" ", "_")
        )

        chunk_id = (
            f"{safe_document_name}"
            f"_p{page_number}"
            f"_c{chunk_number}"
        )

        all_chunks.append({
            "chunk_id": chunk_id,
            "document": document_name,
            "page": page_number,
            "chunk_number": chunk_number,
            "text": chunk_text
        })


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Created {len(all_chunks)} chunks")
print(f"Saved to: {OUTPUT_FILE}")