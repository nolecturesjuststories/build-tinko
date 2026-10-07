# ✂️ Part 1, step 1.6: cut every document into small passages.
#
# Why not search whole documents? Because the answer to a question is usually one paragraph. A small passage that
# is ALL about the question ranks higher than a long letter that mentions it once, and it's what we show as the
# source. So we cut along the structure Document Intelligence already found:
#
#   • forms and tables (a bill, a report card, a recipe card, a telegram) stay whole: they're already one answer
#   • prose (letters, diary pages, agreements) is cut at paragraphs, the natural pieces of what someone wrote
#   • a heading sticks to the text under it, and a table is NEVER cut: half a bill is useless
#   • tiny pieces are merged with their neighbour, so a passage always has enough to say
#   • every passage starts with a one-line header (title · date) so a piece from the middle of a letter
#     still says what it's from
#
# Every passage keeps its document's labels (from tags.json) plus where it came from (source file and page),
# so search can filter by year or person and the assistant can cite the exact page.
#
#   python chunk.py      → passages.jsonl (one passage per line)
import html
import json
import os
import re

MIN_CHARS = 180  # merge pieces smaller than this with the next one
MAX_CHARS = 450  # aim for prose passages around this size
PROSE = {"letter", "diary", "house_paper", "official_letter"}  # everything else is a form: kept whole


def tables_to_markdown(text):
    """Document Intelligence returns tables as HTML; a compact Markdown table says the same in far fewer characters."""
    def convert(m):
        rows = re.findall(r"<tr>(.*?)</tr>", m.group(0), re.S)
        lines = []
        for i, row in enumerate(rows):
            cells = [html.unescape(c.strip()) for c in re.findall(r"<t[hd]>(.*?)</t[hd]>", row, re.S)]
            lines.append("| " + " | ".join(cells) + " |")
            if i == 0:
                lines.append("|" + "---|" * len(cells))
        return "\n".join(lines)
    return re.sub(r"<table>.*?</table>", convert, text, flags=re.S)


def blocks(markdown):
    """Split Markdown into blocks: whole tables, headings, and paragraphs."""
    text = re.sub(r"<!--.*?-->", "", markdown)  # page headers/numbers Document Intelligence marks as comments
    text = re.sub(r"</?figure>", "", text)  # stamps and signatures: keep their words, drop the tag
    text = tables_to_markdown(text)  # a table becomes one block with no blank lines inside: never split
    return [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]


def chunk(markdown, doc_type):
    parts = blocks(markdown)
    if doc_type not in PROSE or len("\n\n".join(parts)) <= MAX_CHARS:
        return ["\n\n".join(parts)]  # a form, or very short prose: keep it whole
    passages, cur = [], ""
    for b in parts:
        heading = cur.startswith("#") and "\n" not in cur  # a heading waits for the text under it
        if cur and not heading and len(cur) >= MIN_CHARS and len(cur) + len(b) > MAX_CHARS:
            passages.append(cur)
            cur = ""
        cur = (cur + "\n\n" + b).strip()
    if cur:
        if passages and len(cur) < MIN_CHARS // 2:
            passages[-1] += "\n\n" + cur  # a last little line (a signature) joins the passage before it
        else:
            passages.append(cur)
    return passages


def main():
    with open("tags.json") as f:
        tags = json.load(f)
    total = 0
    with open("passages.jsonl", "w") as out:
        for name in sorted(tags):
            labels = tags[name]
            with open(os.path.join("markdown", name + ".md")) as f:
                pieces = chunk(f.read(), labels["doc_type"])
            for n, text in enumerate(pieces, 1):
                header = f"[{labels['title']} · {labels['date'] or labels['year']}]"
                out.write(json.dumps({
                    "id": f"{name}-{n}",
                    "content": header + "\n" + text,
                    "source": name + ".pdf",
                    "page": 1,  # every document in the trunk is one page
                    "doc_type": labels["doc_type"],
                    "date": labels["date"],
                    "year": labels["year"],
                    "people": labels["people"],
                    "places": labels["places"],
                    "title": labels["title"],
                }, ensure_ascii=False) + "\n")
            total += len(pieces)
            print(f"  ✂️  {name:28s} → {len(pieces)} passage{'s' if len(pieces) > 1 else ''}")
    print(f"\n{len(tags)} documents → {total} passages → passages.jsonl")


if __name__ == "__main__":
    main()
