# 🔧 Run me first! I check that everything for "Grandma's Trunk" is ready:
#    your Python, the packages, your .env file, and all three Azure services.
#    Each service gets one tiny test call (a few words), so this costs almost nothing.
#    I never print your keys.
import importlib.util
import os
import sys

ok = True


def good(msg):
    print("  ✅ " + msg)


def bad(msg, *fixes):
    global ok
    ok = False
    print("  ❌ " + msg)
    for fix in fixes:
        print("     → " + fix)


# ── 1. Python ─────────────────────────────────────────────────────────────────────────────────
print("\n1️⃣  Python")
if sys.version_info >= (3, 10):
    good("Python " + sys.version.split()[0])
else:
    bad("Python " + sys.version.split()[0] + " is too old: you need 3.10 or newer.",
        "Install the latest from https://www.python.org/downloads/")
    sys.exit(1)

# ── 2. Packages ───────────────────────────────────────────────────────────────────────────────
print("\n2️⃣  Packages")
PACKAGES = {
    "azure.ai.documentintelligence": "azure-ai-documentintelligence",
    "azure.search.documents": "azure-search-documents",
    "openai": "openai",
    "dotenv": "python-dotenv",
}
missing = [pip for module, pip in PACKAGES.items() if importlib.util.find_spec(module) is None]
if missing:
    bad("Missing: " + ", ".join(missing), "Run:  pip install -r requirements.txt")
    sys.exit(1)
good("All packages installed")

# ── 3. Your .env file ─────────────────────────────────────────────────────────────────────────
print("\n3️⃣  Your .env file")
from dotenv import load_dotenv

if not os.path.exists(".env"):
    bad("No .env file in this folder.",
        "Copy the example:  cp .env.example .env   (Windows: copy .env.example .env)",
        "Then paste in your endpoints and keys from the Azure portal.")
    sys.exit(1)
load_dotenv(".env")

NEEDED = [
    "AZURE_DOCINTEL_ENDPOINT", "AZURE_DOCINTEL_KEY",
    "AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_KEY",
    "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_KEY",
    "AZURE_OPENAI_CHAT_DEPLOYMENT", "AZURE_OPENAI_EMBED_DEPLOYMENT",
]
empty = [name for name in NEEDED if not os.getenv(name) or "<" in os.getenv(name)]
if empty:
    bad("Still empty or a placeholder: " + ", ".join(empty),
        "Open .env and replace each <...> with your real value.")
    sys.exit(1)
good("All 8 settings filled in (keys stay hidden)")


def hint(err):
    """Turn a raw error into a fix a beginner can act on."""
    text = str(err)
    if "401" in text or "Unauthorized" in text or "Access denied" in text or "invalid subscription key" in text.lower():
        return "The key looks wrong. Copy KEY 1 again from the portal (Keys and Endpoint)."
    if "404" in text or "DeploymentNotFound" in text or "does not exist" in text:
        return "Not found. Check the endpoint, and that the deployment name matches the one in Foundry."
    if "getaddrinfo" in text or "Name or service not known" in text or "nodename" in text or "Failed to resolve" in text or "Connection error" in text:
        return "Can't reach that address. Check the endpoint: copy it again from the portal."
    if "429" in text:
        return "Too many requests (free tier limit). Wait a minute and run me again."
    return text[:200]


# ── 4. The three Azure services ───────────────────────────────────────────────────────────────
print("\n4️⃣  Azure services (one tiny test call each)")
from azure.core.credentials import AzureKeyCredential

# Document Intelligence: ask for the resource details (no document is read, so no pages are used).
try:
    from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient

    admin = DocumentIntelligenceAdministrationClient(
        os.environ["AZURE_DOCINTEL_ENDPOINT"], AzureKeyCredential(os.environ["AZURE_DOCINTEL_KEY"]))
    admin.get_resource_details()
    good("Document Intelligence is ready to read the trunk")
except Exception as err:
    bad("Document Intelligence: " + hint(err))

# AI Search: list the indexes (a brand-new service has none yet, and that's fine).
try:
    from azure.search.documents.indexes import SearchIndexClient

    search = SearchIndexClient(os.environ["AZURE_SEARCH_ENDPOINT"], AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))
    names = list(search.list_index_names())
    good("AI Search is ready (" + str(len(names)) + " indexes so far)")
except Exception as err:
    bad("AI Search: " + hint(err))

# Azure OpenAI (Foundry): one embedding and one 5-word chat reply.
try:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["AZURE_OPENAI_KEY"],
                    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/")
    vector = client.embeddings.create(model=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"], input="Grandma's kheer recipe")
    good("Embeddings work: '" + os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"] + "' turned 3 words into "
         + str(len(vector.data[0].embedding)) + " numbers")
    reply = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        messages=[{"role": "user", "content": "Say hello to Grandma in five words."}],
        max_completion_tokens=300,  # gpt-5.x models think first; leave room for the reply
        reasoning_effort="low",
    )
    good("Chat works: '" + os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"] + "' says: " + (reply.choices[0].message.content or "(an empty reply, but the call worked)").strip())
except Exception as err:
    bad("Azure OpenAI: " + hint(err))

# ── Result ────────────────────────────────────────────────────────────────────────────────────
print()
if ok:
    print("🎉 All green! The trunk is ready to be read. Next: read_docs.py (Part 1, step 1.4)")
else:
    print("🔧 Fix the ❌ lines above, then run me again. (Nothing was created or charged.)")
    sys.exit(1)
