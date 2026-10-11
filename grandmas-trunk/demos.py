# 🎬 Part 2: the "before" pictures. Three small experiments that show WHY the assistant needs each step.
#
#   python demos.py jumble      2.1  plain search (Part 1), no filter: what Grandma would have to read
#   python demos.py no_pages    2.2  the same model with and without the trunk's pages in its message
#   python demos.py one_prompt  2.3  everything in one prompt: search once, answer once, no checks, no tools
import sys

from azure.search.documents.models import VectorizedQuery

from clients import embeddings, llm, search
from nodes.answer import build_prompt


def hybrid(question, top=6):
    vector = VectorizedQuery(vector=embeddings.embed_query(question), k_nearest_neighbors=50, fields="content_vector")
    return [dict(r) for r in search.search(search_text=question, vector_queries=[vector], top=top, select=["id", "content", "source", "page", "year"])]


def chat(messages):
    return llm.invoke(messages).content.strip()


def jumble(question="What happened in 1975?"):
    print(f"❓ {question}   (plain hybrid search, no filter)")
    for p in hybrid(question):
        print(f"  📄 {p['id']:22s} year {p['year']}  {len(p['content'].split())} words")


def no_pages(question="When did Grandpa move to Mumbai?"):
    print(f"❓ {question}\n\n🙈 without the trunk's pages:")
    print("  " + chat([("human", question)]))
    print("\n📄 with the pages search found:")
    print("  " + chat(build_prompt(question, hybrid(question, 3))))


def one_prompt(question="How much did we spend on electricity in 1985?"):
    passages = hybrid(question)
    print(f"❓ {question}   (one search, one answer)")
    print("  found: " + ", ".join(p["id"] for p in passages))
    print("  💬 " + chat(build_prompt(question, passages)))


if __name__ == "__main__":
    {"jumble": jumble, "no_pages": no_pages, "one_prompt": one_prompt}[sys.argv[1]]()
