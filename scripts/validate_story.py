import json,re
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'app/src/main/assets'
e=json.loads((p/'episode.json').read_text())
cards={c['id']:c for c in e['cards']}
assert all(re.fullmatch('[a-z0-9-]{1,60}',id) for id in cards), 'Card IDs must match the Android pack schema'
assert all(1 <= c['step'] <= e['cardCount'] and len(c['text']) <= 1500 for c in cards.values())
assert len(cards)==len(e['cards'])
paths=[]
def visit(id,path,choices):
    assert id not in path,'Cycle'
    c=cards[id]
    assert (p/c['image']).is_file(),c['image']
    path=path+[id]
    if c.get('ending'):
        paths.append((path,choices));return
    if 'choices' in c:
        for o in c['choices']:visit(o['next'],path,choices+[o['label']])
    else:visit(c['next'],path,choices)
visit(e['start'],[],[])
assert len(paths)==4
for path,choices in paths:
    assert len(path)==18,(len(path),path)
    assert [cards[i]['step'] for i in path]==list(range(1,19))
    assert len(choices)==2
print('PASS: 4 complete story paths; 18 cards and 2 choices each; all images present.')
