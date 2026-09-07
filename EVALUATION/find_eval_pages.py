import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PAGES_FILE = (
    PROJECT_ROOT
    / "DATA"
    / "PROCESSED"
    / "clean_pages.json"
)

with open(PAGES_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)


topics = {
    "battery": [
        "built-in battery",
        "battery defective",
        "rechargeable battery"
    ],
    "bios": [
        "BIOS",
        "UEFI"
    ],
    "windows_recovery": [
        "Windows recovery",
        "recovery",
        "restore Windows"
    ],
    "hardware_replacement": [
        "replace a CRU",
        "before you replace",
        "replacement"
    ],
    "headphones": [
        "headphones",
        "earphones"
    ],
    "support": [
        "technical support",
        "Lenovo support",
        "Customer Support Center"
    ],
    "ports": [
        "HDMI",
        "Thunderbolt",
        "USB-A"
    ]
}


for topic, keywords in topics.items():

    print("\n" + "=" * 80)
    print(f"TOPIC: {topic}")

    matches = []

    for page in pages:

        text_lower = page["text"].lower()

        if any(
            keyword.lower() in text_lower
            for keyword in keywords
        ):
            matches.append({
                "document": page["document"],
                "page": page["page"],
                "text": page["text"][:300]
            })

    for match in matches[:8]:
        print(
            f"\n{match['document']} "
            f"PAGE {match['page']}"
        )
        print(match["text"])