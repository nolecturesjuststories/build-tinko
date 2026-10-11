# 🗺️ Part 2, step 2.3: the agent, as a graph (LangGraph). We write the plan (the boxes and arrows); LangGraph runs it.
#
#   route ──LLM chose a bills tool?──▶ call_api (our .NET API) ───────▶ END
#     │ LLM chose search_trunk
#     ▼
#   retrieve ──▶ grade ──good passages?──▶ answer ──▶ END
#      ▲            │
#      │            └──none passed, tries left?──▶ rewrite ──┐
#      └─────────────────────────────────────────────────────┘
#
# The STATE is the notebook passed from step to step: the question, the clues, the passages, the grades, the answer.
# Each step reads it and writes its part. The arrows with a question (conditional edges) pick what happens next.
#
#   python graph.py "When did Grandpa get his first job?"
import json
import operator
import sys
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from nodes.answer import answer
from nodes.grade import grade
from nodes.retrieve import retrieve
from nodes.rewrite import rewrite
from nodes.route import route
from nodes.call_api import call_api

MAX_RETRIES = 2  # rewrite at most twice, then answer honestly with what we have (maybe "I couldn't find that")


class State(TypedDict, total=False):
    question: str
    tool_call: dict  # the tool the LLM chose in route
    messages: list  # the conversation with the LLM, for a tool call
    clues: dict
    filter: str | None
    query: str
    tried: Annotated[list, operator.add]  # every search query used so far
    tries: int
    passages: list
    relevant: list
    answer: str
    sources: list
    trace: Annotated[list, operator.add]  # what each step did, in order (for the video and for debugging)


def after_route(state):
    return "retrieve" if state["tool_call"]["name"] == "search_trunk" else "call_api"


def after_grade(state):
    if state["relevant"] or state["tries"] >= MAX_RETRIES:
        return "answer"
    return "rewrite"


g = StateGraph(State)
for name, step in [("route", route), ("retrieve", retrieve), ("grade", grade), ("rewrite", rewrite), ("answer", answer), ("call_api", call_api)]:
    g.add_node(name, step)
g.add_edge(START, "route")
g.add_conditional_edges("route", after_route, ["call_api", "retrieve"])
g.add_edge("retrieve", "grade")
g.add_conditional_edges("grade", after_grade, ["answer", "rewrite"])
g.add_edge("rewrite", "retrieve")
g.add_edge("answer", END)
g.add_edge("call_api", END)
assistant = g.compile()


def ask(question):
    return assistant.invoke({"question": question, "tries": 0, "tried": [question], "trace": []})


def show(result):
    for t in result["trace"]:
        step = t["step"]
        if step == "route" and t["tool"] == "search_trunk":
            print(f"  🧭 route     LLM chose search_trunk, clues {json.dumps(t['clues'])}  →  filter: {t['filter']}")
        elif step == "route":
            print(f"  🧭 route     LLM chose {t['tool']}({json.dumps(t['args'])})")
        elif step == "retrieve":
            print(f"  🔍 retrieve  \"{t['query']}\"  →  {', '.join(t['found']) or '(nothing)'}")
        elif step == "grade":
            for gr in t["grades"]:
                print(f"     {'✅' if gr['relevant'] else '❌'} {gr['id']:22s} {gr['reason']}")
        elif step == "rewrite":
            print(f"  ✏️  rewrite   → \"{t['query']}\"" + (f"  (and drop the filter: {t['dropped_filter']})" if t.get("dropped_filter") else ""))
        elif step == "api":
            print(f"  🏢 .NET API  {t['request']}  →  {json.dumps(t['result'])[:110]}")
    print(f"\n💬 {result['answer']}")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "When did Grandpa get his first job?"
    print(f"❓ {q}")
    show(ask(q))
