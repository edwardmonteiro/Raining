"""Validate every reading route and build a reproducible, reader-compatible ZIP."""
import json,re,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'episodes/02-a-mulher-da-estacao'
OUT=ROOT/'dist/Raining-Episodio-02-A-mulher-da-estacao.zip'
e=json.loads((SRC/'episode.json').read_text(encoding='utf-8'))
valid_id=lambda s: isinstance(s,str) and re.fullmatch(r'[a-z0-9-]{1,60}',s)
assert e['schemaVersion']==1 and valid_id(e['id']) and e['episode']==2
assert 0<len(e['title'])<=100 and 1<=e['cardCount']<=100
assert len((SRC/'episode.json').read_bytes())<=200000
assert 1<=len(e['cards'])<=150
cards={c['id']:c for c in e['cards']}
assert len(cards)==len(e['cards'])
images={e['cover']}
for c in cards.values():
    assert valid_id(c['id']) and 0<len(c['text'])<=1500
    assert 1<=c['step']<=e['cardCount']
    assert sum(['next' in c,'choices' in c,c.get('ending',False)])==1
    images.add(c['image'])
    if 'next' in c: assert c['next'] in cards
    if 'choices' in c:
        assert 2<=len(c['choices'])<=4
        for o in c['choices']:
            assert o['next'] in cards and 0<len(o['label'])<=100 and 0<len(o['memory'])<=300
for name in images:
    assert re.fullmatch(r'art/[a-zA-Z0-9_-]+\.(jpg|png|webp)',name)
    assert (SRC/name).is_file()
paths=[]
def walk(id,route,decisions):
    assert id not in route,'Cycle'
    route=route+[id];c=cards[id]
    assert c['step']==len(route),'Skipped/repeated visible step'
    if c.get('ending'):
        assert len(route)==e['cardCount'] and decisions==2
        paths.append(route);return
    for n in ([c['next']] if 'next' in c else [o['next'] for o in c['choices']]):
        walk(n,route,decisions+('choices' in c))
walk(e['start'],[],0)
assert len(paths)==4 and set(sum(paths,[]))==set(cards),'Unreachable cards or missing route'
names=['episode.json']+sorted(images)
assert len(names)<=150
assert all((SRC/n).stat().st_size<=8000000 for n in names)
assert sum((SRC/n).stat().st_size for n in names)<=40000000
OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names:
        info=zipfile.ZipInfo(n,date_time=(2026,10,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
        z.writestr(info,(SRC/n).read_bytes())
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None and set(z.namelist())==set(names)
    assert json.loads(z.read('episode.json'))==e
counts=[sum(len(cards[id]['text'].split()) for id in p) for p in paths]
print(f'PASS: {len(paths)} complete paths, 18 cards and 2 choices each, {min(counts)}–{max(counts)} words, {len(images)} images')
print(f'{hashlib.sha256(OUT.read_bytes()).hexdigest()}  {OUT.name} ({OUT.stat().st_size} bytes)')
