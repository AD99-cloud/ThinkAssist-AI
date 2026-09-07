from pathlib import Path
import json

from SRC.retriever import retrieve


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_FILE = (
    PROJECT_ROOT
    / "EVALUATION"
    / "retrieval_dataset.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "EVALUATION"
    / "retrieval_results.json"
)


with open(DATASET_FILE, "r", encoding="utf-8") as f:
    test_cases = json.load(f)


results = []

top_1_hits = 0
top_3_hits = 0


for test_case in test_cases:

    question = test_case["question"]

    retrieved = retrieve(
        query=question,
        top_k=3
    )

    expected_document = test_case["expected_document"]
    expected_pages = test_case["expected_pages"]

    def is_correct(chunk):
        return (
            chunk["document"] == expected_document
            and chunk["page"] in expected_pages
        )

    top_1_hit = is_correct(retrieved[0])

    top_3_hit = any(
        is_correct(chunk)
        for chunk in retrieved
    )

    if top_1_hit:
        top_1_hits += 1

    if top_3_hit:
        top_3_hits += 1

    results.append({
        "question": question,
        "expected_document": expected_document,
        "expected_pages": expected_pages,
        "top_1_hit": top_1_hit,
        "top_3_hit": top_3_hit,
        "retrieved": [
            {
                "document": chunk["document"],
                "page": chunk["page"],
                "distance": round(
                    chunk["distance"],
                    4
                )
            }
            for chunk in retrieved
        ]
    })


total = len(test_cases)

summary = {
    "total_tests": total,
    "top_1_retrieval_accuracy": round(
        top_1_hits / total,
        3
    ),
    "top_3_retrieval_accuracy": round(
        top_3_hits / total,
        3
    )
}


output = {
    "summary": summary,
    "results": results
}


with open(
    RESULTS_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        output,
        f,
        indent=2,
        ensure_ascii=False
    )


print("\nRETRIEVAL EVALUATION")
print("=" * 50)

for key, value in summary.items():
    print(f"{key}: {value}")

print()
print(f"Results saved to: {RESULTS_FILE}")