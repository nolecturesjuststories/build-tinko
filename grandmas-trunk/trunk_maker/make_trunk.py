"""Fill the trunk: render every document in content.py to ../trunk/<id>.pdf and write ../trunk/catalog.json.

Usage (from the grandmas-trunk folder):  python trunk_maker/make_trunk.py [--only id1,id2] [--preview]
--preview also saves a small PNG of each first page in trunk_maker/preview/ for a quick look.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from content import DOCS  # noqa: E402
from render import LAYOUTS, save_pdf  # noqa: E402

OUT = os.path.join(HERE, '..', 'trunk')


def main():
    only = None
    if '--only' in sys.argv:
        only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
    preview = '--preview' in sys.argv
    os.makedirs(OUT, exist_ok=True)
    if preview:
        os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    catalog = []
    for doc in DOCS:
        if only and doc['id'] not in only:
            continue
        pages = LAYOUTS[doc['layout']](doc)
        save_pdf(pages, os.path.join(OUT, doc['id'] + '.pdf'))
        if preview:
            p = pages[0]
            p.thumbnail((900, 900))
            p.save(os.path.join(HERE, 'preview', doc['id'] + '.png'))
        catalog.append({'file': doc['id'] + '.pdf', 'pages': len(pages), **doc['meta']})
        print(f"  {doc['id']:28s} {doc['layout']:10s} {len(pages)} page(s)")
    if not only:
        with open(os.path.join(OUT, 'catalog.json'), 'w') as f:
            json.dump(catalog, f, indent=1)
    print(f'{len(catalog)} documents → {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
