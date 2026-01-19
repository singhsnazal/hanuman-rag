import re
from langsmith import Client
from langsmith.evaluation import evaluate

from rag.chain import answer_question


# ✅ PREDICT FUNCTION (your model output)
def predict(inputs: dict) -> dict:
    q = inputs["question"]
    answer, sources, contexts = answer_question(q)
    return {"answer": answer, "sources": sources}


# ✅ Evaluator 1: Answer relevance (simple heuristic)
def eval_answer_relevance(run, example):
    """
    Checks if answer is empty or generic.
    """
    answer = (run.outputs.get("answer") or "").strip().lower()

    if len(answer) < 10:
        score = 0
        comment = "Answer too short / empty"
    else:
        score = 1
        comment = "Answer has content"

    return {"key": "answer_relevance", "score": score, "comment": comment}


# ✅ Evaluator 2: Hallucination check for trick questions
def eval_hallucination(run, example):
    """
    If question asks personal info not in resume (DOB/salary/father),
    answer should say 'not mentioned'.
    """
    q = example.inputs["question"].lower()
    answer = (run.outputs.get("answer") or "").lower()

    trick_patterns = ["date of birth", "dob", "salary", "father", "pan", "aadhaar"]
    is_trick = any(p in q for p in trick_patterns)

    if is_trick:
        if "not mentioned" in answer or "not available" in answer or "not provided" in answer:
            return {"key": "hallucination", "score": 1, "comment": "Correctly refused / not mentioned"}
        else:
            return {"key": "hallucination", "score": 0, "comment": "Likely hallucinated: should say not mentioned"}
    else:
        return {"key": "hallucination", "score": 1, "comment": "Not a trick question"}


# ✅ Evaluator 3: Conciseness check
def eval_conciseness(run, example):
    answer = (run.outputs.get("answer") or "")
    word_count = len(answer.split())

    # simple scoring
    if word_count <= 120:
        return {"key": "conciseness", "score": 1, "comment": f"Concise ({word_count} words)"}
    else:
        return {"key": "conciseness", "score": 0, "comment": f"Too long ({word_count} words)"}


if __name__ == "__main__":
    client = Client()

    results = evaluate(
        predict,
        data="resume_eval_set",  # ✅ dataset name
        evaluators=[eval_answer_relevance, eval_hallucination, eval_conciseness],
        experiment_prefix="resume_rag_eval",
        client=client,
    )

    print("✅ Experiment completed. Check LangSmith → Experiments.")
    print(results)
