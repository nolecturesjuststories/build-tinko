# 🏢 Part 2, step 2.8: call the .NET API. The LLM asked for a bills tool; the agent makes the real HTTP call
# (GET /bills/sum?year=1985), hands the result back to the LLM, and the LLM writes the answer.
import json

from langchain_core.messages import ToolMessage

from agent_tools import API_TOOLS, ENDPOINT
from clients import llm

RULES = "Answer in one or two short sentences, in rupees (Rs), using only the tool's result. Cite the bills as [first bill … last bill]."


def call_api(state):
    call = state["tool_call"]
    result = API_TOOLS[call["name"]].invoke(call["args"])  # ← the HTTP call to our .NET API
    messages = [*state["messages"], ToolMessage(json.dumps(result), tool_call_id=call["id"])]
    reply = llm.invoke([("system", RULES), *messages[1:]])
    text = reply.content.strip()
    bills = result.get("bills", [result]) if isinstance(result, dict) else result
    request = f"{ENDPOINT[call['name']]}?{'&'.join(f'{k}={v}' for k, v in call['args'].items())}"
    return {"answer": text, "sources": sorted({b["source"] for b in bills if "source" in b}),
            "trace": [{"step": "api", "request": request, "result": result, "answer": text}]}
