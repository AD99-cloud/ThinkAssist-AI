from pathlib import Path
import json
import time

from SRC.assistant import ask


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_FILE = PROJECT_ROOT / "EVALUATION" / "dataset.json"
RESULTS_FILE = PROJECT_ROOT / "EVALUATION" / "results.json"


with open(DATASET_FILE, "r", encoding="utf-8") as f:
    test_cases = json.load(f)


results = []

answer_type_correct = 0
grounding_correct = 0
tool_correct = 0
source_correct = 0

total_latency = 0


for test_case in test_cases:

    question = test_case["question"]

    start = time.perf_counter()

    response = ask(question)

    latency_ms = (time.perf_counter() - start) * 1000

    total_latency += latency_ms

    # Answer type
    type_match = (
        response["answer_type"]
        == test_case["expected_answer_type"]
    )

    if type_match:
        answer_type_correct += 1

    # Grounding
    grounding_match = (
        response["grounded"]
        == test_case["expected_grounded"]
    )

    if grounding_match:
        grounding_correct += 1

    # Tool selection
    tool_match = (
        response["tool_used"]
        == test_case["expected_tool"]
    )

    if tool_match:
        tool_correct += 1

    # Source check
    expected_document = test_case["expected_document"]

    if expected_document is None:
        source_match = True
    else:
        returned_documents = [
            source["document"]
            for source in response["sources"]
        ]

        source_match = (
            expected_document in returned_documents
        )

    if source_match:
        source_correct += 1

    results.append({
        "question": question,
        "answer": response["answer"],
        "answer_type": response["answer_type"],
        "expected_answer_type": test_case["expected_answer_type"],
        "answer_type_correct": type_match,
        "grounded": response["grounded"],
        "expected_grounded": test_case["expected_grounded"],
        "grounding_correct": grounding_match,
        "tool_used": response["tool_used"],
        "expected_tool": test_case["expected_tool"],
        "tool_correct": tool_match,
        "source_correct": source_match,
        "latency_ms": round(latency_ms, 2)
    })


total = len(test_cases)

summary = {
    "total_tests": total,
    "answer_type_accuracy": round(
        answer_type_correct / total,
        3
    ),
    "grounding_accuracy": round(
        grounding_correct / total,
        3
    ),
    "tool_selection_accuracy": round(
        tool_correct / total,
        3
    ),
    "source_accuracy": round(
        source_correct / total,
        3
    ),
    "average_latency_ms": round(
        total_latency / total,
        2
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


print("\nEVALUATION SUMMARY")
print("=" * 50)

for key, value in summary.items():
    print(f"{key}: {value}")

print()
print(f"Results saved to: {RESULTS_FILE}")