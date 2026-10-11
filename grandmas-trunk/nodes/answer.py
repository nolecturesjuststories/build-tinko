# 💬 Part 2, step 2.7: answer, with proof. The passages that passed the check are pasted into the model's message
# (that's the "augmented" in retrieval-augmented generation), with three rules: only from the passages, cite
# [source, page] for every fact, and say so when the answer isn't there.
from clients import llm

RULES = (
    "You are Grandma's trunk assistant. Answer the question using ONLY the passages below, from the family's old papers. "
    "Rules:\n"
    "1. Use only facts written in the passages. Never add facts from your own knowledge.\n"
    "2. After every fact, cite where it came from as [source, p.N].\n"
    "3. If the passages don't contain the answer, say: \"I couldn't find that in the trunk.\"\n"
    "Answer in one to three short sentences. Grandpa is Mohan, Grandma is Kamla."
)


def build_prompt(question, passages):
    pages = "\n\n".join(f"[{p['source']}, p.{p['page']}]\n{p['content']}" for p in passages) or "(no passages found)"
    return [("system", RULES), ("human", f"Passages:\n\n{pages}\n\nQuestion: {question}")]


def answer(state):
    passages = state.get("relevant") or []
    text = llm.invoke(build_prompt(state["question"], passages)).content.strip()
    return {"answer": text, "sources": sorted({p["source"] for p in passages}),
            "trace": [{"step": "answer", "used": [p["id"] for p in passages], "answer": text}]}
