#!/usr/bin/env python3
"""Catch catalogue/search/export drift and accidental URL regressions."""
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
raw = (ROOT / 'data/catalogue.json.gz').read_bytes()
cat = json.loads(gzip.decompress(raw))
index = json.loads((ROOT / 'data/search-index.json').read_text(encoding='utf-8'))
expected = {(i['class_code'], i['subclass_code'], i['zh'], i['en'], i['code']) for i in cat['items']}
indexed = {(str(i[0]).zfill(2), i[1], i[2], i[3], i[4]) for i in index['items']}
assert expected == indexed, 'Search index does not match source catalogue'
with (ROOT / 'data/nice-classification-zh-en.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
exported = {(i['class_code'], i['subclass_code'], i['item_zh'], i['item_en'], i['item_code']) for i in rows}
assert expected == exported, 'CSV does not match source catalogue'
assert len(index['classes']) == len(cat['classes']) == 45
assert len(index['subclasses']) == len(cat['subclasses'])
assert all('*' not in i[2] and '*' not in i[3] for i in expected), 'Unexpected stars in goods names'
assert all(i[3] == 'tops [clothing]' for i in expected if i[2] == '上衣'), 'Outdated tops translation'
assert any(i[2] == '上衣' for i in expected)
for cls in index['classes']:
    assert cls[3] and (ROOT / 'classification' / cls[3]).is_file(), f'Missing class page: {cls}'
manifest = dict(source_revision=cat.get('revision'), source_sha256=hashlib.sha256(raw).hexdigest(),
                classes=len(cat['classes']), similar_groups=len(cat['subclasses']), items=len(index['items']))
(ROOT / 'data/build-info.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print('Validated source, index, exports and class URLs:', manifest)
