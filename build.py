#!/usr/bin/env python3
"""Gabungkan data kosakata dan bunpou dari semua tingkat (N5 sampai N1) menjadi dist/index.html.

Cara pakai:
    python3 build.py

Nama file harus mengikuti pola:
    data/kotoba/kotoba-n5.json, kotoba-n4.json, ... kotoba-n1.json
    data/bunpou/bunpou-n5.json, bunpou-n4.json, ... bunpou-n1.json
Satu tingkat boleh punya lebih dari satu file, misalnya kotoba-n5-bab1.json.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TEMPLATE = ROOT / 'template' / 'reader.html'
OUT = ROOT / 'dist' / 'index.html'
LEVEL_RE = re.compile(r'-(n[1-5])(?:-[^.]*)?\.json$', re.IGNORECASE)
LEVEL_ORDER = {'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3, 'N1': 4}


def level_of(path):
    m = LEVEL_RE.search(path.name)
    if not m:
        print(f'  peringatan: {path.name} tidak punya tingkat di namanya (contoh: kotoba-n5.json), dilewati')
        return None
    return m.group(1).upper()


def read_list(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        data = data.get('entries') or data.get('items') or []
    if not isinstance(data, list):
        sys.exit(f'{path.name}: harus berupa daftar JSON (array).')
    return data


def files(folder, prefix):
    found = []
    for f in (ROOT / 'data' / folder).glob(f'{prefix}-*.json'):
        lvl = level_of(f)
        if lvl:
            found.append((LEVEL_ORDER[lvl], f.name, f, lvl))
    return [(lvl, f, name) for _, name, f, lvl in sorted(found)]


def load_kotoba():
    entries, seen, names, counts = [], {}, [], {}
    for lvl, f, name in files('kotoba', 'kotoba'):
        names.append(name)
        for e in read_list(f):
            e['level'] = lvl
            key = str(e.get('id', e.get('guid')))
            if key in seen:
                print(f'  peringatan: id {key} ganda di {name} dan {seen[key]}')
            seen[key] = name
            if not e.get('word') and not e.get('reading'):
                print(f'  peringatan: entri {key} di {name} tidak punya word atau reading')
            entries.append(e)
            counts[lvl] = counts.get(lvl, 0) + 1
    meta = {'source': ', '.join(names) or '-', 'schema': 'clean', 'totalEntries': len(entries), 'levels': counts}
    return {'meta': meta, 'entries': entries}


def load_bunpou():
    items, counts = [], {}
    for lvl, f, name in files('bunpou', 'bunpou'):
        for g in read_list(f):
            g.setdefault('jlpt_level', lvl)
            if not g.get('grammar_point'):
                print(f'  peringatan: pola tanpa grammar_point di {name}')
            items.append(g)
            counts[lvl] = counts.get(lvl, 0) + 1
    return items, counts


def embed(obj):
    text = json.dumps(obj, ensure_ascii=False)
    return text.replace('</', '<\\/').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def main():
    kotoba = load_kotoba()
    bunpou, bcounts = load_bunpou()
    html = TEMPLATE.read_text(encoding='utf-8')
    for placeholder in ('/*DATA*/', '/*GRAMMAR*/'):
        if html.count(placeholder) != 1:
            sys.exit(f'template harus memuat tepat satu {placeholder}')
    html = html.replace('/*DATA*/', embed(kotoba), 1).replace('/*GRAMMAR*/', embed(bunpou), 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding='utf-8')
    kc = kotoba['meta']['levels']
    print('kosakata per tingkat: ' + (', '.join(f'{k} {v}' for k, v in sorted(kc.items(), key=lambda x: LEVEL_ORDER[x[0]])) or '-'))
    print('bunpou per tingkat:   ' + (', '.join(f'{k} {v}' for k, v in sorted(bcounts.items(), key=lambda x: LEVEL_ORDER[x[0]])) or '-'))
    print(f'ditulis ke {OUT}')


if __name__ == '__main__':
    main()
