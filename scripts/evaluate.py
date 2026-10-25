import json
import sys
from pathlib import Path

# Add the project root to Python's import path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion import build_chunks
from src.retrieval import PolicyRetriever


def main():
    # Build the policy document index
    chunks = build_chunks()
    retriever = PolicyRetriever(chunks)

    # Load evaluation questions
    evaluation_file = ROOT / "data" / "evaluation" / "questions.json"

    with open(evaluation_file, "r", encoding="utf-8") as file:
        questions = json.load(file)

    correct = 0

    for item in questions:
        results = retriever.search(
            query=item["question"],
            top_k=5,
            role=item["role"],
            region=item["region"],
        )

        expected_id = item["expected_doc_id"]

        found = any(
            result["doc_id"] == expected_id
            for result in results
        )

        if found:
            correct += 1

        top_result = results[0]["doc_id"] if results else "NONE"

        status = "PASS" if found else "FAIL"

        print(
            f"[{status}] "
            f"Expected={expected_id} | "
            f"Top result={top_result} | "
            f"Question={item['question']}"
        )

    total = len(questions)

    if total:
        print("\nEvaluation Summary")
        print("------------------")
        print(f"Correctly retrieved: {correct}/{total}")
        print(f"Recall@5: {correct / total:.2%}")

    print(
        "\nNote: This is a small demonstration dataset, "
        "not a production accuracy benchmark."
    )


if __name__ == "__main__":
    main()