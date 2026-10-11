# 🔍 Part 2, step 2.5: retrieve (the RAG part). The same hybrid search as Part 1 (words + meaning) in Azure AI Search,
# with the filter the LLM chose.
from azure.search.documents.models import VectorizedQuery

from clients import embeddings, search

TOP = 6


def retrieve(state):
    vector = VectorizedQuery(vector=embeddings.embed_query(state["query"]), k_nearest_neighbors=50, fields="content_vector")
    results = search.search(search_text=state["query"], vector_queries=[vector], filter=state["filter"], top=TOP,
                            select=["id", "content", "source", "page", "year", "doc_type"])
    passages = [{k: r[k] for k in ("id", "content", "source", "page", "year", "doc_type")} for r in results]
    return {"passages": passages,
            "trace": [{"step": "retrieve", "query": state["query"], "filter": state["filter"], "found": [p["id"] for p in passages]}]}
