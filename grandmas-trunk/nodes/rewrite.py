# ✏️ Part 2, step 2.6: rewrite. Nothing passed the check, so ask again with the words the DOCUMENT would use,
# and search the whole trunk this time: the route's filter may have been too strict.
from clients import ask_json

SCHEMA = {
    "type": "object",
    "properties": {"query": {"type": "string"}},
    "required": ["query"],
    "additionalProperties": False,
}

INSTRUCTIONS = (
    "A search over old family papers (letters, diaries, bills, report cards, official letters, recipes, telegrams) "
    "found nothing useful. Rewrite the question as a short search query using the words the document itself would "
    "probably contain. Grandpa is Mohan (M. K. Joshi), Grandma is Kamla."
)


def rewrite(state):
    tried = "\n".join(f"- {q}" for q in state["tried"])
    new = ask_json(INSTRUCTIONS, f"Question: {state['question']}\nQueries already tried:\n{tried}", "rewrite", SCHEMA)["query"]
    return {"query": new, "filter": None, "tries": state["tries"] + 1, "tried": [new],
            "trace": [{"step": "rewrite", "query": new, "dropped_filter": state["filter"]}]}
