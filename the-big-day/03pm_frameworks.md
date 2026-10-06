# ⏰ 3:00 PM: Frameworks (LangGraph and CrewAI)

No code to run in this scene. Read this, then compare it with `02pm_loop.py`.

## The 2 PM loop, redrawn as a graph

In `02pm_loop.py` we wrote the loop by hand: think → act → check → repeat.
A framework like **LangGraph** lets you *draw* that same loop as a graph:

- **Nodes** are steps: `think`, `act`, `check`.
- **Edges** are arrows: "after think, go to...".
- A **conditional edge** is a fork in the road: *"Need a tool?"* Yes → `act`. No → `END`.
- **Shared state** is one notebook every node reads and writes (the messages, the batter, the step count).

```
         +------------------------------------------+
         v                                          |
START -> think --"need a tool?"-- yes --> act --> check
         |
         no
         v
        END

 shared state: { messages, batter, steps }
```

Same idea as our `while not done:` loop. The graph just makes it easier to see,
pause, save, and grow (add a "taste test" node, a human-approval node, ...).

## Preview, real code in B11

This is **LangGraph-style pseudocode** (a preview, not runnable here):

```python
graph = StateGraph(KitchenState)          # the shared state

graph.add_node("think", think)            # each node = a plain function
graph.add_node("act", act)
graph.add_node("check", check)

graph.add_edge(START, "think")
graph.add_conditional_edges(              # the fork: "need a tool?"
    "think",
    need_a_tool,                          # returns "act" or "end"
    {"act": "act", "end": END},
)
graph.add_edge("act", "check")
graph.add_edge("check", "think")          # loop back, like while not done

app = graph.compile()
app.invoke({"messages": ["Bake a cake for Rohan"]})
```

## CrewAI: a team instead of one cook (real code in B12)

**CrewAI** thinks in people, not arrows. You describe **roles** (a ChefBot who bakes,
a ShopperBot who buys, a DecoBot who decorates), give them **tasks** ("buy candles",
"bake the cake"), and put them in a **crew** that runs the tasks and hands results
from one agent to the next. You'll see a hand-made version of this at 6 PM in
`06pm_team.py`, and the real CrewAI version in B12.

---
🔁 Make it real: build these graphs and crews with a real local AI in Season B.
🎬 Full build: Season B, episode B11 LangGraph and episode B12 CrewAI (team)
