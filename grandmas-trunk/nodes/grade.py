# ✅ Part 2, step 2.6: grade. The model as a checker: the question + each passage → relevant or not, and why.
# Only passages that pass go on to the answer. (All passages in one request: fewer calls, same verdicts.)
from clients import ask_json

SCHEMA = {
    "type": "object",
    "properties": {
        "grades": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "description": "The passage number"},
                    "relevant": {"type": "boolean"},
                    "reason": {"type": "string", "description": "One short sentence"},
                },
                "required": ["n", "relevant", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["grades"],
    "additionalProperties": False,
}

INSTRUCTIONS = (
    "You check search results for Grandma's family-papers assistant. For EACH numbered passage, decide on its own "
    "whether it helps answer the question (it contains the answer or a needed part of it). "
    "Grandpa is Mohan, Grandma is Kamla."
)


def grade(state):
    passages = state["passages"]
    if not passages:
        return {"relevant": [], "trace": [{"step": "grade", "grades": []}]}
    listed = "\n\n".join(f"Passage {n} ({p['source']}):\n{p['content']}" for n, p in enumerate(passages, 1))
    verdicts = {g["n"]: g for g in ask_json(INSTRUCTIONS, f"Question: {state['question']}\n\n{listed}", "grades", SCHEMA)["grades"]}
    grades = [verdicts.get(n, {"relevant": False, "reason": "not graded"}) for n in range(1, len(passages) + 1)]
    relevant = [p for p, g in zip(passages, grades) if g["relevant"]]
    return {"relevant": relevant,
            "trace": [{"step": "grade", "grades": [{"id": p["id"], "relevant": g["relevant"], "reason": g["reason"]} for p, g in zip(passages, grades)]}]}
