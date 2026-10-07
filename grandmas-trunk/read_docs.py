# 📖 Part 1, step 1.4: read every document in the trunk with Azure AI Document Intelligence.
#
# Every page in the trunk looks different: handwriting, printed tables, forms, stamps. The "prebuilt-layout" model
# reads them all and gives back the same kind of thing for each one: clean Markdown text (paragraphs, headings,
# tables) plus details such as which parts were handwritten.
#
#   python read_docs.py                  read everything in trunk/ (skips files already read)
#   python read_docs.py letter_1968_03   read just one document (by name)
#
# Output:  markdown/<name>.md     the text, ready for the next steps
#          markdown/<name>.json   the full result (pages, tables, handwriting spans), for the curious
#
# Free tier (F0): 500 pages a month and 20 requests a minute, so we pause 3.5 s between documents.
import json
import os
import sys
import time

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentContentFormat
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
client = DocumentIntelligenceClient(os.environ["AZURE_DOCINTEL_ENDPOINT"], AzureKeyCredential(os.environ["AZURE_DOCINTEL_KEY"]))

TRUNK = "trunk"
OUT = "markdown"
os.makedirs(OUT, exist_ok=True)


def read(name):
    """Send one PDF to Document Intelligence and save what it read."""
    with open(os.path.join(TRUNK, name + ".pdf"), "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",  # the general model: text, tables, structure, handwriting
            f,
            output_content_format=DocumentContentFormat.MARKDOWN,  # tables come back as Markdown tables
        )
    result = poller.result()

    with open(os.path.join(OUT, name + ".md"), "w") as f:
        f.write(result.content)
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(result.as_dict(), f, indent=1)

    handwritten = sum(1 for s in result.styles or [] if s.is_handwritten)
    return len(result.pages), len(result.tables or []), handwritten > 0


def main():
    names = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(TRUNK) if f.endswith(".pdf"))
    pages = done = skipped = 0
    errors = []
    for i, name in enumerate(names):
        if len(sys.argv) == 1 and os.path.exists(os.path.join(OUT, name + ".md")):
            skipped += 1
            continue
        try:
            n_pages, n_tables, hand = read(name)
            pages += n_pages
            done += 1
            extra = (f", {n_tables} table" + ("s" if n_tables > 1 else "")) if n_tables else ""
            print(f"  ✅ {name:28s} {n_pages} page{'s' if n_pages > 1 else ''}{extra}{', handwriting ✍️' if hand else ''}")
        except Exception as err:  # keep going: one bad file shouldn't stop the whole trunk
            errors.append(name)
            print(f"  ❌ {name}: {str(err)[:160]}")
        if i < len(names) - 1:
            time.sleep(3.5)  # stay under the free tier's 20 requests a minute
    print(f"\nread {done} documents · {pages} pages · {len(errors)} errors" + (f" · {skipped} already read" if skipped else ""))
    if errors:
        print("Run again to retry: " + " ".join(errors))


if __name__ == "__main__":
    main()
