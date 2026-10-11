# 🧭 Part 2, step 2.4: route. The LLM reads the question and CHOOSES A TOOL, filling in its inputs:
#
#   search_trunk(query, year?, doc_type?, people?)   → the clues become search FILTERS (year eq 1975 …)
#   bills_sum(year) / bills_highest / bills_list      → a .NET API call, for exact numbers
#
# This is what makes it an agent: the LLM decides what happens next.
from langchain_core.messages import HumanMessage, SystemMessage

from agent_tools import ALL_TOOLS
from clients import llm

INSTRUCTIONS = (
    "You are the agent behind Grandma's trunk assistant. Choose exactly one tool for the question. "
    "Questions about electricity totals, the highest bill, or listing bills use the bills tools; everything else "
    "searches the trunk. Grandpa is Mohan, Grandma is Kamla. When searching, add a filter only when the question "
    "clearly gives it (a year, a kind of document, or documents about a person); most questions need few or none."
)


def to_filter(clues):
    """Clues → an Azure AI Search filter, e.g. "year eq 1975 and doc_type eq 'letter'"."""
    parts = []
    if clues.get("year"):
        parts.append(f"year eq {clues['year']}")
    if clues.get("doc_type"):
        parts.append(f"doc_type eq '{clues['doc_type']}'")
    for person in clues.get("people") or []:
        parts.append(f"people/any(p: p eq '{person}')")
    return " and ".join(parts) or None


def route(state):
    messages = [SystemMessage(INSTRUCTIONS), HumanMessage(state["question"])]
    choice = llm.bind_tools(ALL_TOOLS, tool_choice="any").invoke(messages)
    call = choice.tool_calls[0]
    if call["name"] == "search_trunk":
        clues = {k: call["args"].get(k) for k in ("year", "doc_type", "people")}
        return {"tool_call": call, "clues": clues, "filter": to_filter(clues), "query": state["question"],
                "trace": [{"step": "route", "tool": "search_trunk", "clues": clues, "filter": to_filter(clues)}]}
    return {"tool_call": call, "messages": [*messages, choice],
            "trace": [{"step": "route", "tool": call["name"], "args": call["args"]}]}
