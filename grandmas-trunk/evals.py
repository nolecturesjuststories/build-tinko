# 📝 Part 3, step 3.2: the exam. 25 questions with known answers (trunk/ground_truth.json), run through the assistant,
# each checked three ways:
#
#   answer    does it contain the key fact ("1968")? and a judge model compares it with the right answer
#   source    did it cite (one of) the right documents?
#   refusal   for questions the trunk can't answer, did it say "I couldn't find that"?
#
#   python evals.py            → the report card, plus outputs/eval_<time>.json with every answer
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from clients import ask_json
from graph import ask

REFUSAL = "couldn't find"

JUDGE = (
    "You mark an exam. The correct answer is a reference. The assistant's answer passes if it correctly answers what "
    "the QUESTION asks. Leaving out reference details the question didn't ask for is fine; extra true detail is fine. "
    "It fails if it gets a fact wrong, contradicts the reference, or misses the main thing the question asks for."
)
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"correct": {"type": "boolean"}, "reason": {"type": "string"}},
    "required": ["correct", "reason"],
    "additionalProperties": False,
}


def mark(q):
    r = ask(q["question"])
    text = r["answer"]
    if q["kind"] == "refuse":
        ok_answer = REFUSAL in text.lower()
        ok_source, why = True, "refused" if ok_answer else "answered instead of refusing"
    else:
        hits = [m for m in q["must_contain"] if m.lower() in text.lower()]
        has_fact = bool(hits) if q.get("match") == "any" else len(hits) == len(q["must_contain"])
        judge = ask_json(JUDGE, f"Question: {q['question']}\nCorrect answer: {q['answer']}\nAssistant's answer: {text}", "mark", JUDGE_SCHEMA)
        ok_answer = has_fact and judge["correct"]
        ok_source = bool(set(r.get("sources") or []) & set(q["sources"]))
        why = judge["reason"] if not ok_answer else ("" if ok_source else "right answer, wrong citation")
    return {"id": q["id"], "kind": q["kind"], "question": q["question"], "expected": q["answer"], "answer": text,
            "sources": r.get("sources"), "passed": ok_answer and ok_source, "answer_ok": ok_answer, "source_ok": ok_source,
            "why": why, "trace": r["trace"]}


def main():
    questions = json.load(open("trunk/ground_truth.json"))["questions"]
    with ThreadPoolExecutor(1) as pool:
        results = list(pool.map(mark, questions))
    print("\n📝 Report card\n")
    for r in results:
        print(f"  {'✅' if r['passed'] else '❌'} {r['id']:2d} {r['kind']:8s} {r['question'][:58]:58s}" + ("" if r["passed"] else f"\n        → {r['answer'][:110]}\n        ✗ {r['why'][:110]}"))
    kinds = sorted({r["kind"] for r in results}, key=[q["kind"] for q in questions].index)
    print("\n  " + " · ".join(f"{k} {sum(r['passed'] for r in results if r['kind'] == k)}/{sum(r['kind'] == k for r in results)}" for k in kinds))
    print(f"\n  Score: {sum(r['passed'] for r in results)}/{len(results)}")
    os.makedirs("outputs", exist_ok=True)
    path = f"outputs/eval_{time.strftime('%Y%m%d_%H%M%S')}.json"
    json.dump(results, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"  every answer → {path}")


if __name__ == "__main__":
    main()
