# 🔌 Part 2: the connections every step shares, read from .env.
#
#   • LangChain (langchain-openai) is the plug to the LLM: gpt-5.4-mini for thinking and writing,
#     text-embedding-3-small for turning a question into numbers. The LLM itself runs in Azure, not here.
#   • Azure AI Search holds the trunk's passages (built in Part 1).
#   • TRUNK_TOOLS_URL is our .NET API (TrunkTools/), the tools the agent can call for exact numbers.
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()
BASE_URL = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/"
KEY = os.environ["AZURE_OPENAI_KEY"]
llm = ChatOpenAI(model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"], base_url=BASE_URL, api_key=KEY,
                 reasoning_effort="low", max_retries=8)  # free-tier rate limits: wait and retry instead of failing
embeddings = OpenAIEmbeddings(model=os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"], base_url=BASE_URL, api_key=KEY,
                              check_embedding_ctx_length=False, max_retries=8)
search = SearchClient(os.environ["AZURE_SEARCH_ENDPOINT"], "grandmas-trunk", AzureKeyCredential(os.environ["AZURE_SEARCH_KEY"]))
TRUNK_TOOLS_URL = os.environ.get("TRUNK_TOOLS_URL", "http://localhost:5085")


def ask_json(instructions, message, name, schema):
    """Ask the LLM to fill in a fixed form (a JSON schema), like the labels in Part 1."""
    form = llm.with_structured_output({"title": name, **schema}, method="json_schema", strict=True)
    return form.invoke([("system", instructions), ("human", message)])
