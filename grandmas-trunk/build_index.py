# 🔎 Part 1, step 1.7: store every passage in Azure AI Search, as words AND as meaning.
#
#   • as words: the passage text is searchable by keywords ("Bombay", "kheer", "1975")
#   • as meaning: text-embedding-3-small turns each passage into 1536 numbers (an embedding). Passages that MEAN
#     similar things get similar numbers, so "moved to Mumbai" lands right next to "shifted to Bombay".
#   • as labels: doc_type, year, people and places are filterable ("only diaries from 1975")
#   • a synonym map tells keyword search that Bombay and Mumbai are the same city
#
#   python build_index.py      → creates (or recreates) the index "grandmas-trunk" and uploads every passage
import json
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    SynonymMap,
    VectorSearch,
    VectorSearchProfile,
)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
INDEX = "grandmas-trunk"
search_key = AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"])
indexes = SearchIndexClient(os.environ["AZURE_SEARCH_ENDPOINT"], search_key)
ai = OpenAI(api_key=os.environ["AZURE_OPENAI_KEY"], base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/")
EMBED = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]

# 1. The synonym map: old and new names of the same places (Solr format, one group per line).
indexes.create_or_update_synonym_map(SynonymMap(name="trunk-places", synonyms=[
    "Bombay, Mumbai",
    "Madras, Chennai",
    "Calcutta, Kolkata",
]))

# 2. The index: what we store for each passage, and what each field can do.
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String, synonym_map_names=["trunk-places"]),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,  # text-embedding-3-small gives 1536 numbers
        vector_search_profile_name="meaning",
    ),
    SimpleField(name="doc_type", type=SearchFieldDataType.String, filterable=True, facetable=True),
    SimpleField(name="date", type=SearchFieldDataType.String),
    SimpleField(name="year", type=SearchFieldDataType.Int32, filterable=True, facetable=True, sortable=True),
    SearchField(name="people", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True, facetable=True),
    SearchField(name="places", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SimpleField(name="source", type=SearchFieldDataType.String),
    SimpleField(name="page", type=SearchFieldDataType.Int32),
]
vector_search = VectorSearch(
    algorithms=[HnswAlgorithmConfiguration(name="hnsw")],  # a fast "nearest neighbours" lookup
    profiles=[VectorSearchProfile(name="meaning", algorithm_configuration_name="hnsw")],
)
if INDEX in indexes.list_index_names():
    indexes.delete_index(INDEX)  # start fresh so re-running gives the same result
indexes.create_index(SearchIndex(name=INDEX, fields=fields, vector_search=vector_search))
print(f"  ✅ index '{INDEX}' created (content, content_vector[1536], doc_type, year, people, places, source, page)")

# 3. Embed every passage (in batches of 16) and upload it.
passages = [json.loads(line) for line in open("passages.jsonl")]
search = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], INDEX, search_key)
for i in range(0, len(passages), 16):
    batch = passages[i : i + 16]
    vectors = ai.embeddings.create(model=EMBED, input=[p["content"] for p in batch]).data
    for p, v in zip(batch, vectors):
        p["content_vector"] = v.embedding
    results = search.upload_documents(batch)
    print(f"  ⬆️  uploaded {i + len(batch):3d} / {len(passages)}  ({sum(r.succeeded for r in results)} ok)")

print(f"\n{len(passages)} passages in the index '{INDEX}', searchable by words and by meaning")
