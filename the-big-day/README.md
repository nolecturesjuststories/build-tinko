# 🪔 Tinko's Big Day: the code

**Watched the film? Run every scene yourself.** 🎬 Watch it here: https://youtu.be/DxJQE4YxvY4

One day. Rohan's birthday, on Diwali, with Grandma flying in. Tinko the AI agent helps with
everything, and every hour of the film teaches one AI-agent idea. Each scene below is one small
Python file you can run, read, and change.

No installs. No API keys. No internet. Just Python 3.10+.

## 🎬 The scenes

| Film time | File | The idea | Full build in Season B |
|-----------|------|----------|------------------------|
| 7:00 AM | `07am_memory.py` | Short-term vs long-term memory (a diary file) | B4 Memory |
| 7:30 AM | `0730_agent.py` | What an agent is: brain + tools + loop | B1–B3 Your first agent |
| 12:00 PM | `12pm_tool_call.py` | Tool calling: the JSON "order slip" | B2 Tool calling |
| 1:00 PM | `01pm_rag.py` | RAG: look it up before you answer | B5 RAG |
| 2:00 PM | `02pm_loop.py` | The agent loop: think, act, check | B3 The agent loop |
| 3:00 PM | `03pm_frameworks.md` | The loop as a graph (LangGraph) + teams (CrewAI) *(read, don't run)* | B11 LangGraph, B12 CrewAI |
| 5:00 PM | `05pm_planning.py` | Plan first, then re-plan when a step fails | B6 Planning |
| 5:30 PM | `0530pm_mcp_server.py` | MCP: a universal plug for AI tools | B7 MCP |
| 6:00 PM | `06pm_team.py` | Multi-agent: a manager and a team of bots | B12 CrewAI (team) |
| 6:30 PM | `0630pm_guardrails.py` | Guardrails + a human says yes or no | B8 Guardrails |
| 9:00 PM | `09pm_evals.py` | Evals: Tinko's driving test | B9 Evals |
| 10:00 PM | `10pm_ship.py` | Shipping: logs, a budget, alerts | B10 Ship it |

Shared helper: `toy_brain.py` (see below). Setup checker: `check_setup.py`.

## ⚡ Setup in 5 minutes

1. **Get Python 3.10 or newer** from [python.org/downloads](https://www.python.org/downloads/).
   - **Windows:** on the first install screen, tick **"Add Python to PATH"**.
   - **Mac / Linux:** you may already have it. Check with `python3 --version`.
2. **Download this repo** (green **Code** button → **Download ZIP**, then unzip) and open a
   terminal inside the `the-big-day` folder.
3. **Check your setup:**
   - Windows: `py check_setup.py`
   - Mac / Linux: `python3 check_setup.py`
4. **Run a scene**, for example `python3 12pm_tool_call.py` (Windows: `py 12pm_tool_call.py`).

**Can't install anything?** (school laptop, tablet, ...) Open this repo in
[GitHub Codespaces](https://github.com/features/codespaces) (green **Code** button → **Codespaces**),
or use [Google Colab](https://colab.research.google.com/): upload the files from this folder (folder icon on the
left), then run a scene in a cell with `!python 12pm_tool_call.py`. Both are free and run in your browser.

## 🗺️ Suggested order

Follow the film: top to bottom in the table. If you only have 10 minutes, run these three:
`12pm_tool_call.py` → `02pm_loop.py` → `0630pm_guardrails.py`.

Then try a challenge: in `09pm_evals.py` one test fails on purpose. Fix `toy_brain.py` so it scores 10/10.

## 🧸 About ToyBrain

`toy_brain.py` is a **pretend brain**. A real AI (an LLM) understands your words; ToyBrain just
looks for keywords. We use it so everything runs instantly with zero setup, and it talks
exactly like a real AI does: plain text answers, or JSON tool calls.

In **Season B** you swap `ToyBrain()` for a real AI that runs free on your own laptop
(with [Ollama](https://ollama.com/)). The rest of the code stays almost the same. That's the point!

Two files are created when you run the scenes: `tinko_diary.json` (7 AM) and `tinko.log` (10 PM).
Delete them any time.
