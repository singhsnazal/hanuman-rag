import json
from rag.chain import answer_question

with open("eval/questions.json", "r") as f:
    tests = json.load(f)

results = []

for t in tests:
    q = t["question"]
    expected = t["expected"]

    answer, sources, contexts = answer_question(q)

    results.append({
        "question": q,
        "expected": expected,
        "answer": answer,
        "sources": sources
    })

with open("eval/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Evaluation results saved to eval/results.json")
