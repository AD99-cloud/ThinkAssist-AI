from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SPECS_FILE = (
    PROJECT_ROOT
    / "DATA"
    / "Processed"
    / "device_specs.json"
)


with open(SPECS_FILE, "r", encoding="utf-8") as f:
    DEVICE_DATA = json.load(f)


def lookup_device_spec(category: str, item: str):

    category = category.lower().strip()
    item = item.lower().strip()

    category_data = DEVICE_DATA.get(category)

    if not category_data:
        return {
            "found": False,
            "message": f"Unknown specification category: {category}"
        }

    value = category_data.get(item)

    if value is None:
        return {
            "found": False,
            "message": f"No specification found for {item}"
        }

    return {
        "found": True,
        "category": category,
        "item": item,
        "value": value
    }