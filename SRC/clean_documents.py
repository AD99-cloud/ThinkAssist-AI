from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "DATA" / "Processed"

input_file = PROCESSED_DIR / "pages.json"
output_file = PROCESSED_DIR / "clean_pages.json"


def clean_text(text: str) -> str:
    # Replace strange PDF bullet characters
    text = text.replace("", "- ")

    # Normalize Windows-style line endings
    text = text.replace("\r", "\n")

    # Remove spaces before line breaks
    text = re.sub(r"[ \t]+\n", "\n", text)

    # Collapse 3+ line breaks into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse repeated spaces inside lines
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


with open(input_file, "r", encoding="utf-8") as f:
    pages = json.load(f)

cleaned_pages = []

for page in pages:
    cleaned_pages.append({
        "document": page["document"],
        "page": page["page"],
        "text": clean_text(page["text"])
    })

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        cleaned_pages,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Cleaned {len(cleaned_pages)} pages")
print(f"Saved to: {output_file}")