# 🧳 Grandma's Trunk: build an AI archive assistant

Grandma's trunk holds sixty years of family papers: handwritten letters, recipe cards, a diary, bills, report cards.
We build an assistant that reads all of it and answers questions like *"When did Grandpa move to Mumbai?"*, citing the
exact page. It's a real RAG build with the stack Azure teams use:

- **Azure AI Document Intelligence** reads every layout (handwriting, tables, forms)
- **Azure AI Search** finds passages by words *and* by meaning
- **Azure OpenAI in Microsoft Foundry**: `text-embedding-3-small` + `gpt-4.1-mini`
- **LangGraph** for the assistant's logic, **Streamlit** for the chat screen

All the documents in the trunk are fictional, generated with code, so every answer can be checked.

## 🛡️ Safety first (before you create anything)

1. **Set a budget alarm.** Azure portal → Cost Management → **Budgets** → Add: **$10 a month**, with an email alert at
   **80%**. New subscriptions can take a day or two before budgets unlock: wait for it.
2. **Choose the free tiers.** Document Intelligence: **Free F0** (500 pages a month). AI Search: **Free**. The portal
   pre-selects *Standard* for AI Search (about $250 a month): click **Change Pricing Tier → Free**.
3. **Keys stay in `.env`.** Never in your code, never in a screenshot, never on GitHub (`.env` is already in
   `.gitignore`).
4. **Clean up when you're done**: delete the resource group, and everything in it goes.

## ⚡ Setup

1. **Python 3.10+** from [python.org/downloads](https://www.python.org/downloads/).
2. In the Azure portal, create one resource group (e.g. `grandmas-trunk-rg`) with:
   - **Document Intelligence**, pricing tier **Free F0**
   - **AI Search**, pricing tier **Free**
   - a **Microsoft Foundry** resource with two model deployments: **`text-embedding-3-small`** and **`gpt-4.1-mini`**
3. Open a terminal in this folder and install the packages (all versions pinned):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Copy the settings file and fill in your endpoints and keys (each resource → **Keys and Endpoint**):
   ```bash
   cp .env.example .env             # Windows: copy .env.example .env
   ```
5. **Check everything:**
   ```bash
   python check_setup.py
   ```
   You should see four sections of ✅ ending in **"All green!"**. Each ❌ tells you exactly what to fix.

## 🗺️ The plan

```
trunk (scans) → read (Document Intelligence) → tag → cut into passages → index (AI Search) → ask
```

- **Part 1: From trunk to index**: read every layout, tag, chunk, build the hybrid index
- **Part 2: The assistant**: LangGraph agentic RAG with citations, a bill-adding tool, the Streamlit chat
- **Part 3: Make it trustworthy**: evals, "I don't know" answers, costs, a free local path (pgvector)

*No Azure account? Part 3 shows a free path with pgvector in Docker.*
