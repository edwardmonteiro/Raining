"""Read both complementary routes: covers all 20 unique illustrated cards."""
import json,re,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
PKG='com.raining.story';PACK='Raining-Episodio-03-O-retrato-que-faltava.zip'
e=json.loads(Path('episodes/03-o-retrato-que-faltava/episode.json').read_text());cards={c['id']:c for c in e['cards']}
Path('screenshots').mkdir(exist_ok=True)
def adb(*args):return subprocess.check_output(['adb',*args],text=True)
def tree():
    adb('shell','uiautomator','dump','/sdcard/window.xml')
    return ET.fromstring(adb('shell','cat','/sdcard/window.xml'))
def texts():return ET.tostring(tree(),encoding='unicode')
def click(part,scroll=True,exact=False):
    for _ in range(5 if scroll else 1):
        root=tree()
        for n in root.iter('node'):
            if ((part.casefold()==n.get('text','').casefold() if exact else part.casefold() in n.get('text','').casefold()) or part.casefold()==n.get('content-desc','').casefold()) and n.get('enabled')=='true':
                b=list(map(int,re.findall(r'\d+',n.get('bounds'))))
                adb('shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2));time.sleep(.3);return
        if scroll:adb('shell','input','swipe','500','1750','500','750','250')
    raise AssertionError('Missing '+part+'; '+ET.tostring(root,encoding='unicode'))
def shot(name):Path('screenshots/ep3-'+name+'.png').write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p']))
def home():adb('shell','input','keyevent','4');time.sleep(.3)
def launch():adb('shell','am','start','-n',PKG+'/.MainActivity');time.sleep(1)
def run():
    adb('install','-r','dist/Raining-v0.1.0.apk');adb('shell','wm','size','1080x2400');adb('shell','wm','density','420');adb('shell','pm','clear',PKG);adb('logcat','-c')
    adb('push','dist/'+PACK,'/sdcard/Download/'+PACK)
    launch();click('Começar');click('Próximo card');home();click('Episódios');click('Importar pack de episódio');time.sleep(1)
    if PACK not in texts():click('Show roots',False);click('Downloads',False)
    click(PACK);time.sleep(1);assert e['title'] in texts();shot('home')
    seen=set()
    for branch in [0,1]:
        if branch==0:click('Começar')
        else:
            home();click('Revisitar');click('Recomeçar',False,True)
        id=e['start'];choices=0
        while True:
            card=cards[id];view=texts()
            assert f"{card['step']:02d} / 18" in view,(id,view)
            assert 'Ilustração indisponível' not in view,id
            seen.add(id)
            if id in ['shop','portrait','album','apron','doorbell'] or id in ['last-visit','opening','regret','joke']:shot(id)
            if branch==0 and card['step']==6:
                adb('shell','am','force-stop',PKG);launch();click('Continuar');assert '06 / 18' in texts()
            if card.get('ending'):
                click('Guardar este capítulo');assert 'CAPÍTULO GUARDADO' in texts();shot('ending-'+str(branch));break
            if 'choices' in card:
                selected=card['choices'][branch];click(selected['label']);id=selected['next'];choices+=1
            else:click('Próximo card');id=card['next']
        assert choices==2
        print('PASS route',branch,flush=True)
    assert seen==set(cards),'Not all illustrations rendered'
    home();click('Episódios');click('01 · Uma mesa para dois');click('Continuar');assert '02 / 18' in texts()
    assert 'FATAL EXCEPTION' not in adb('logcat','-d','-s','AndroidRuntime:E')
    print('PASS: real ZIP import, all 20 illustrated nodes, both branches, saved ending, process-death resume, preserved episode 1 progress.',flush=True)
try:run()
except Exception:
    shot('failure');print(texts(),flush=True);print(adb('logcat','-d','-s','AndroidRuntime:E'),flush=True);raise
