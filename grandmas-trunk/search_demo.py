# 🔍 Part 1, step 1.8: the first search. One question, three ways, side by side.
#
#   • keyword: matches the words in the question (plus our synonym map: Bombay = Mumbai)
#   • vector:  matches the MEANING: the question becomes 1536 numbers and we find the nearest passages
#   • hybrid:  runs both and merges the two rankings (Reciprocal Rank Fusion)
#
#   python search_demo.py                                   → the demo question
#   python search_demo.py "What did Grandma cook for Diwali?" → any question you like
import os
import sys

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
search = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], "grandmas-trunk", AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))
ai = OpenAI(api_key=os.environ["AZURE_OPENAI_KEY"], base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/")
EMBED = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]
TOP = 3


def first_line(text):
    """The passage's first real line after the [title · date] header, for a one-line preview."""
    body = [ln.strip() for ln in text.split("\n")[1:] if ln.strip() and not ln.startswith("#")]
    return (body[0] if body else "")[:60]


def show(name, results):
    print(f"\n{name}")
    for rank, r in enumerate(results, 1):
        print(f"  {rank}. {r['id']:22s} {first_line(r['content'])}")


question = sys.argv[1] if len(sys.argv) > 1 else "When did Grandpa move to Mumbai?"
print(f"❓ {question}")
vector = VectorizedQuery(
    vector=ai.embeddings.create(model=EMBED, input=question).data[0].embedding,
    k_nearest_neighbors=50,  # look at plenty of neighbours so the hybrid merge has enough to work with
    fields="content_vector",
)

show("🔤 keyword", search.search(search_text=question, top=TOP))
show("🧭 vector", search.search(search_text=None, vector_queries=[vector], top=TOP))
show("🔀 hybrid", search.search(search_text=question, vector_queries=[vector], top=TOP))
