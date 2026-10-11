# 🧳 Grandma's Trunk: build an AI archive assistant

Grandma's trunk holds sixty years of family papers: handwritten letters, recipe cards, a diary, bills, report cards.
We build an assistant that reads all of it and answers questions like *"When did Grandpa move to Mumbai?"*, citing the
exact page. It's a real RAG build with the stack Azure teams use:

- **Azure AI Document Intelligence** reads every layout (handwriting, tables, forms)
- **Azure AI Search** finds passages by words *and* by meaning
- **Azure OpenAI in Microsoft Foundry**: `text-embedding-3-small` + `gpt-5.4-mini`
- **LangGraph** for the assistant's logic, **Streamlit** for the chat screen

All the documents in the trunk are fictional, generated with code, so every answer can be checked.

## 🛡️ Safety first (before you create anything)

1. **Set a budget alarm.** **$10 a month**, with an email alert at **80%** (step 1 below).
2. **Choose the free tiers.** Document Intelligence: **Free F0** (500 pages a month). AI Search: **Free**. The portal
   pre-selects *Standard* for AI Search (about $250 a month): click **Change Pricing Tier → Free**.
3. **Keys stay in `.env`.** Never in your code, never in a screenshot, never on GitHub (`.env` is already in
   `.gitignore`).
4. **Clean up when you're done**: delete the resource group, and everything in it goes (see the end of Setup).

## ⚡ Setup, step by step

About 30 minutes. The Azure portal changes its buttons now and then: if a step looks different, the official Microsoft
guide linked in each step has the current screens. Keep all three services in **one resource group** and **one
region**, so clean-up later is a single delete.

### 1. Budget alarm (first, before anything else)

1. In the [Azure portal](https://portal.azure.com), search **Subscriptions** → open your subscription.
2. Left menu: **Cost Management → Budgets → + Add**.
3. **Name** `grandmas-trunk-budget`, **Reset period** Monthly, **Amount** `10` → **Next**.
4. **Alert conditions:** Type **Actual cost**, **80** % (that's $8). **Alert recipients:** your email → **Create**.

> 🕐 Brand-new subscription? If you see *"Failed to retrieve billing information"* and **Add** is greyed out, Azure
> hasn't started your cost data yet. It takes 24–48 hours: come back tomorrow, then continue.
> ([Microsoft guide: create a budget](https://learn.microsoft.com/azure/cost-management-billing/costs/tutorial-acm-create-budgets))

### 2. A resource group

1. Search **Resource groups** → **+ Create**.
2. **Resource group** `grandmas-trunk-rg`, pick a **Region** near you (use the same region in every step) →
   **Review + create** → **Create**.

### 3. Document Intelligence (Free F0)

1. Search **Document Intelligence** → **+ Create**. (A note about "registering Cognitive Services" on a new
   subscription is normal: Azure does it for you.)
2. **Resource group** `grandmas-trunk-rg`, same **Region**, **Name** e.g. `grandmas-trunk-docintel-<your initials>`
   (it must be unique worldwide).
3. **Pricing tier: Free F0** (500 pages a month). → **Review + create** → **Create**.
4. When it's ready: **Go to resource → Keys and Endpoint**. Copy **Endpoint** and **KEY 1** into `.env` as
   `AZURE_DOCINTEL_ENDPOINT` and `AZURE_DOCINTEL_KEY` (step 6).

> Only one Free F0 Document Intelligence resource is allowed per subscription.
> ([Microsoft guide](https://learn.microsoft.com/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource))

### 4. AI Search (Free) ⚠️ the default is NOT free

1. Search **AI Search** → **+ Create**.
2. **Resource group** `grandmas-trunk-rg`, **Service name** e.g. `grandmas-trunk-search-<your initials>` (lowercase,
   unique), same **Location**.
3. **Pricing tier** shows **Standard** (about $250 a month!). Click **Change Pricing Tier → Free → Select**. Check it now
   says **Free** before you continue.
4. **Review + create** → **Create**.
5. When it's ready: **Overview** → copy the **Url** into `AZURE_SEARCH_ENDPOINT`. **Security + networking → Keys** → copy the
   **Primary admin key** into `AZURE_SEARCH_KEY`.

> Only one Free search service is allowed per subscription. Free = 50 MB and 3 indexes: plenty for the trunk.
> ([Microsoft guide](https://learn.microsoft.com/azure/search/search-create-service-portal) ·
> [tiers and prices](https://learn.microsoft.com/azure/search/search-sku-tier))

### 5. Microsoft Foundry: the two models

These two are pay-per-use, but tiny: building and testing the whole trunk costs cents.

1. Open the [Foundry portal](https://ai.azure.com) and sign in with the same account. The first time, Foundry creates
   a **project** for you (on a Foundry resource). If it asks where, pick `grandmas-trunk-rg`. The region it picks can
   differ from your other services (ours landed in East US 2): that's fine.
2. Top menu **Build → Models → Deployments → Deploy a base model**.
3. Search **`gpt-5.4-mini`** → open it → **Deploy → Custom settings**.
   - **Deployment name:** keep `gpt-5.4-mini` (our code uses this name).
   - **Deployment type:** **Global Standard**. If you see **"Insufficient quota"** (common on new free accounts),
     switch to **Data Zone Standard**: same pay-per-use price, your data is just processed in your region's zone.
   - **Priority processing:** leave it **off** (it costs more). → **Deploy**.
4. Repeat for **`text-embedding-3-small`** (deployment name `text-embedding-3-small`, Global Standard).
5. **Build → Models → Deployments** should now list both as **Succeeded**.
6. Copy the **Azure OpenAI endpoint** (the one that looks like `https://<name>.openai.azure.com`, shown on the project
   **Home** page) and the **API key** (same page, copy button) into `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`.

> Why `gpt-5.4-mini` and not `gpt-4o-mini` / `gpt-4.1-mini`? Those older minis are marked *Deprecated* / *Legacy*
> in Foundry and will be retired; `gpt-5.4-mini` is *Generally available*.
> ([models and regions](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models) ·
> [Microsoft guide: deploy models](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models))

### 6. Python, packages and your `.env`

1. **Python 3.10+** from [python.org/downloads](https://www.python.org/downloads/).
2. Open a terminal in this folder:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env             # Windows: copy .env.example .env
   ```
3. Open `.env` and replace every `<...>` with the endpoints and keys you copied above.

### 7. Check everything

```bash
python check_setup.py
```

You should see four sections of ✅ ending in **"All green!"**. Each ❌ says what to fix:

| You see | Fix |
|---|---|
| `No .env file` / `Still empty or a placeholder` | Step 6: copy `.env.example` to `.env` and fill in every `<...>` |
| `The key looks wrong` | Copy **KEY 1** / the **Primary admin key** again (no spaces) |
| `Can't reach that address` | Copy the endpoint again from the portal |
| `Not found` on Azure OpenAI | The deployment names in `.env` must match the names in Foundry exactly |
| `Too many requests` | Free-tier limit: wait a minute and run it again |

### 🧹 When you're done: clean up

Azure portal → **Resource groups** → `grandmas-trunk-rg` → **Delete resource group** → type the name → **Delete**.
Everything inside goes with it, so nothing keeps running.
([Microsoft guide](https://learn.microsoft.com/azure/azure-resource-manager/management/delete-resource-group))

## 🧳 What's in the trunk

[`trunk/`](trunk) holds 55 fictional family papers from 1962 to 1997, drawn with code to look like old scans
(handwriting, stains, folds, stamps, a slight tilt), so Document Intelligence has real work to do:

| Kind | Count | Layout challenge |
|---|---|---|
| Handwritten letters (Grandpa Mohan, Grandma Kamla, her sister Savitri, Arun, Meera) | 12 | three different hands, dates in prose |
| Electricity bills, Dec 1984 – Jan 1986 | 14 | printed tables; a total needs every bill |
| Grandma's diary pages (1975, 1983, 1991) | 8 | printed date headings + handwriting |
| Recipe cards (including the real kheer) | 6 | short lists, turmeric stains |
| Report cards | 4 | forms: printed labels, handwritten marks |
| House papers (rent agreement, sale deed, tax receipt) and an appointment letter | 4 | dense typewritten text |
| Telegrams and wedding invitations | 6 | strips of capitals, decorative type |
| Ration card | 1 | a household table on a form |

- [`trunk/catalog.json`](trunk/catalog.json): every file with its type, date, people and places.
- [`trunk/ground_truth.json`](trunk/ground_truth.json): 25 questions with known answers and sources, used in Part 3.
- [`trunk_maker/`](trunk_maker): the code that draws the trunk (`python trunk_maker/make_trunk.py`). The family,
  every word and every number are invented; nothing here is a real person's paper.

## 🗺️ The plan

```
trunk (scans) → read (Document Intelligence) → tag → cut into passages → index (AI Search) → ask
```

- **Part 1: From trunk to index**: read every layout, tag, chunk, build the hybrid index
- **Part 2: The assistant**: LangGraph agentic RAG with citations, a bill-adding tool, the Streamlit chat
- **Part 3: Make it trustworthy**: evals, "I don't know" answers, costs, a free local path (pgvector)

*No Azure account? Part 3 shows a free path with pgvector in Docker.*

## 🤖 Part 2: the assistant (an AI agent)

Part 1 built the search. Part 2 turns it into an **agent** that answers Grandma in one sentence, with proof:
the LLM picks a tool, search finds pages, the LLM checks every page, rewrites the question if nothing fits, and
calls a small **.NET API** when it needs exact numbers.

```
question → route (the LLM picks a tool)
              ├─ search_trunk → retrieve (Azure AI Search) → grade each page ──passed──▶ answer, with [source, page]
              │                     ▲                            │ none passed
              │                     └──── rewrite (max 2 tries) ◀┘
              └─ bills_sum / bills_highest / bills_list → the .NET API runs SQL → answer
```

| Script | What it does |
|---|---|
| [`clients.py`](clients.py) | **LangChain** plugs: the LLM (gpt-5.4-mini) and the embedding model, plus Azure AI Search |
| [`agent_tools.py`](agent_tools.py) | the agent's **tools**: `search_trunk` (the RAG tool) and the three bills tools (HTTP calls to the .NET API) |
| [`nodes/`](nodes) | the steps: `route.py` · `retrieve.py` · `grade.py` · `rewrite.py` · `answer.py` · `call_api.py` |
| [`graph.py`](graph.py) | **LangGraph**: the plan (steps, arrows, the retry limit) and the state passed between steps |
| [`load_bills.py`](load_bills.py) | copies the bill amounts the LLM labelled in Part 1 into SQLite: one row per bill |
| [`TrunkTools/`](TrunkTools) | the **.NET API** (ASP.NET Core, .NET 10): `GET /bills/sum`, `/bills/highest`, `/bills`, each one SQL query |
| [`app.py`](app.py) | the **Streamlit** chat, with a Sources box under every answer |
| [`demos.py`](demos.py) | the "before" experiments from the video: no pages, one search, one prompt |
| [`evals.py`](evals.py) | the 25-question exam (used in Part 3) |

**Run it** (after Part 1, with your `.env` filled in; also needs the [.NET 10 SDK](https://dotnet.microsoft.com/download)):

```bash
pip install -r requirements.txt
python load_bills.py                    # the bills table (TrunkTools/trunk.db)
dotnet run --project TrunkTools         # the .NET API on http://localhost:5085 (leave it running)
python graph.py "When did Grandpa get his first job?"   # watch every step of the agent
streamlit run app.py                    # the chat
```

What you should see: *"Grandpa got his first job on Monday, 2nd April 1962… [letter_1962_04.pdf, p.1]"*, and for
*"How much did we spend on electricity in 1985?"* the agent calls `GET /bills/sum?year=1985` and answers
**Rs 1,378 from 13 bills**. Thirteen bills in one year? That's not a typo in this README: it's the bug Part 3 finds. 😉
