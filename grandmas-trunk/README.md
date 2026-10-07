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

1. Search **Document Intelligence** → **+ Create**.
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
5. When it's ready: **Overview** → copy the **Url** into `AZURE_SEARCH_ENDPOINT`. **Settings → Keys** → copy the
   **Primary admin key** into `AZURE_SEARCH_KEY`.

> Only one Free search service is allowed per subscription. Free = 50 MB and 3 indexes: plenty for the trunk.
> ([Microsoft guide](https://learn.microsoft.com/azure/search/search-create-service-portal) ·
> [tiers and prices](https://learn.microsoft.com/azure/search/search-sku-tier))

### 5. Microsoft Foundry: the two models

These two are pay-per-use, but tiny: building and testing the whole trunk costs cents.

1. Open the [Foundry portal](https://ai.azure.com) and create a **project** (it creates a Foundry resource for you).
   Put it in `grandmas-trunk-rg` and the same region.
2. In the project: **Models + endpoints → + Deploy model → Deploy base model**.
3. Pick **`gpt-4.1-mini`** → **Confirm**. **Deployment type: Global Standard**. Keep the **Deployment name**
   `gpt-4.1-mini` (our code uses this name) → **Deploy**.
4. Repeat for **`text-embedding-3-small`** (deployment name `text-embedding-3-small`).
5. Find the **Azure OpenAI endpoint**, the one that looks like `https://<name>.openai.azure.com/`, and the **key**
   (project overview, or the Foundry resource's **Keys and Endpoint** page in the Azure portal). Copy them into
   `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`.

> If a model isn't offered in your region, create the project in a region that has it
> ([models and regions](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models)).
> ([Microsoft guide: deploy models](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models))

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

## 🗺️ The plan

```
trunk (scans) → read (Document Intelligence) → tag → cut into passages → index (AI Search) → ask
```

- **Part 1: From trunk to index**: read every layout, tag, chunk, build the hybrid index
- **Part 2: The assistant**: LangGraph agentic RAG with citations, a bill-adding tool, the Streamlit chat
- **Part 3: Make it trustworthy**: evals, "I don't know" answers, costs, a free local path (pgvector)

*No Azure account? Part 3 shows a free path with pgvector in Docker.*
