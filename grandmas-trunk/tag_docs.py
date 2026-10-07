# 🏷️ Part 1, step 1.5: give every document the same labels.
#
# After step 1.4 every document is Markdown, but a letter, a bill and a diary page still say "when" and "who" in
# completely different ways. Here gpt-5.4-mini reads each one and fills in the SAME small form for all of them:
#
#   doc_type   letter, telegram, recipe, diary, bill, report_card, house_paper, invitation, ration_card, official_letter
#   date       the date written on the document (YYYY-MM-DD, or YYYY-MM / YYYY when that's all it says)
#   year       the year of that date (a number, so search can filter "year eq 1975")
#   people     family members mentioned, first names only (Mohan, Kamla, Arun, Meera, ...)
#   places     towns and cities mentioned
#   title      a short title a person would give it
#   amount     the total amount for bills and receipts, otherwise null
#
# A JSON schema makes the model answer in exactly this shape, every time.
#
#   python tag_docs.py      → tags.json (one entry per document)
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["AZURE_OPENAI_KEY"], base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/")
MODEL = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

DOC_TYPES = ["letter", "telegram", "recipe", "diary", "bill", "report_card", "house_paper", "invitation", "ration_card", "official_letter"]

SCHEMA = {
    "type": "object",
    "properties": {
        "doc_type": {"type": "string", "enum": DOC_TYPES},
        "date": {"type": "string", "description": "The date written on the document: YYYY-MM-DD, or YYYY-MM or YYYY if that is all it gives"},
        "year": {"type": "integer"},
        "people": {"type": "array", "items": {"type": "string"}, "description": "Family members mentioned, first names only"},
        "places": {"type": "array", "items": {"type": "string"}},
        "title": {"type": "string"},
        "amount": {"type": ["number", "null"], "description": "Total amount in rupees for bills and receipts, else null"},
    },
    "required": ["doc_type", "date", "year", "people", "places", "title", "amount"],
    "additionalProperties": False,
}

INSTRUCTIONS = (
    "You label old family papers from Grandma's trunk. The family: Grandpa Mohan (also written M. K. Joshi), "
    "Grandma Kamla, their children Arun and Meera, Kamla's sister Savitri, Grandpa's mother (Amma). "
    "Read the document and fill in the labels. Use only what the document says; never guess."
)


def tag(name, markdown):
    reply = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": f"Document file: {name}.pdf\n\n{markdown}"},
        ],
        response_format={"type": "json_schema", "json_schema": {"name": "labels", "schema": SCHEMA, "strict": True}},
        reasoning_effort="low",
        max_completion_tokens=2000,
    )
    return json.loads(reply.choices[0].message.content)


def main():
    names = sorted(f[:-3] for f in os.listdir("markdown") if f.endswith(".md"))
    tags = {}
    for name in names:
        with open(os.path.join("markdown", name + ".md")) as f:
            labels = tag(name, f.read())
        tags[name] = labels
        print(f"  🏷️  {name:28s} {labels['doc_type']:15s} {labels['date']:11s} {', '.join(labels['people'])[:40]}")
    with open("tags.json", "w") as f:
        json.dump(tags, f, indent=1, ensure_ascii=False)
    print(f"\nlabelled {len(tags)} documents → tags.json")


if __name__ == "__main__":
    main()
