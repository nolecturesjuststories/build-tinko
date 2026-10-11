# 🗄️ Part 2, step 2.8: store the numbers in a database. In Part 1 the LLM read every document once and filled the same
# form for each (tags.json: doc_type, date, year, amount). Words belong in the search index; NUMBERS belong in a table,
# so they can be added up exactly. This copies every bill into SQLite: one row per bill.
#
#   python load_bills.py      → TrunkTools/trunk.db, table bills(source, bill_date, year, amount)
import json
import os
import sqlite3

DB = os.path.join("TrunkTools", "trunk.db")
tags = json.load(open("tags.json"))
rows = [(f"{name}.pdf", t["date"], t["year"], t["amount"]) for name, t in sorted(tags.items()) if t["doc_type"] == "bill" and t["amount"] is not None]

con = sqlite3.connect(DB)
con.execute("DROP TABLE IF EXISTS bills")
con.execute("CREATE TABLE bills (source TEXT PRIMARY KEY, bill_date TEXT, year INTEGER, amount REAL)")
con.executemany("INSERT INTO bills VALUES (?, ?, ?, ?)", rows)
con.commit()
for r in con.execute("SELECT source, bill_date, year, amount FROM bills ORDER BY source"):
    print(f"  🧾 {r[0]:20s} {r[1]:10s} {r[2]}  Rs {r[3]:6.2f}")
print(f"\n{len(rows)} bills → {DB} (table: bills)")
