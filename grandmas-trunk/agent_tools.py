# 🧰 Part 2, step 2.8: the agent's tools. LangChain turns each function below into a tool description (name, what it
# does, its inputs) that the LLM reads. The LLM never runs them: it asks for one, and the agent calls it.
#
#   search_trunk    the RAG tool: search Grandma's trunk (Azure AI Search), with optional filters
#   bills_*         our .NET API (TrunkTools/): exact numbers that search can't add up
import httpx
from langchain_core.tools import tool

from clients import TRUNK_TOOLS_URL


@tool
def search_trunk(query: str, year: int | None = None, doc_type: str | None = None, people: list[str] | None = None) -> str:
    """Search Grandma's trunk of family papers (letters, diaries, recipes, report cards, telegrams, official letters,
    house papers, invitations, bills) by words and meaning. Use year / doc_type / people ONLY when the question clearly
    asks for them. doc_type is one of: letter, telegram, recipe, diary, bill, report_card, house_paper, invitation,
    ration_card, official_letter. people are first names: Mohan (Grandpa), Kamla (Grandma), Arun, Meera, Savitri."""
    return "(the agent's retrieve step runs this search)"


def _get(path, **params):
    r = httpx.get(f"{TRUNK_TOOLS_URL}{path}", params=params, timeout=10)
    if r.status_code != 404:  # "not found" is an answer too (e.g. no bills that year): hand it to the LLM
        r.raise_for_status()
    return r.json()


@tool
def bills_sum(year: int) -> dict:
    """Add up the family's electricity bills for one year (from the .NET API). Returns the total in rupees and the bills used."""
    return _get("/bills/sum", year=year)


@tool
def bills_highest(year: int) -> dict:
    """Find the most expensive electricity bill of one year (from the .NET API)."""
    return _get("/bills/highest", year=year)


@tool
def bills_list(year: int) -> list:
    """List every electricity bill of one year, with its amount (from the .NET API)."""
    return _get("/bills", year=year)


API_TOOLS = {t.name: t for t in (bills_sum, bills_highest, bills_list)}
ENDPOINT = {"bills_sum": "GET /bills/sum", "bills_highest": "GET /bills/highest", "bills_list": "GET /bills"}
ALL_TOOLS = [search_trunk, *API_TOOLS.values()]
