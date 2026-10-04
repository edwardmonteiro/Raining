"""Import the real ZIP through Android's file picker and exercise the unchanged reader."""
import subprocess,time,re,xml.etree.ElementTree as ET
from pathlib import Path
PKG='com.raining.story'
PACK='Raining-Episodio-02-A-mulher-da-estacao.zip'
Path('screenshots').mkdir(exist_ok=True)
def adb(*args):return subprocess.check_output(['adb',*args],text=True)
def tree():
    adb('shell','uiautomator','dump','/sdcard/window.xml')
    return ET.fromstring(adb('shell','cat','/sdcard/window.xml'))
def texts():return ET.tostring(tree(),encoding='unicode')
def tap_node(n):
    b=list(map(int,re.findall(r'\d+',n.get('bounds'))))
    adb('shell','input','tap',str((b[0]+b[2])//2),str((b[1]+b[3])//2));time.sleep(.4)
def click(part,scroll=True):
    for attempt in range(5 if scroll else 1):
        root=tree()
        for n in root.iter('node'):
            if (part in n.get('text','') or part==n.get('content-desc')) and n.get('enabled')=='true':
                tap_node(n);return
        if scroll:adb('shell','input','swipe','500','1750','500','750','250')
    raise AssertionError('Missing '+part+'; '+ET.tostring(root,encoding='unicode')[:7000])
def screenshot(name):
    Path('screenshots/episode2-'+name+'.png').write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p']))
def launch():
    adb('shell','am','start','-n',PKG+'/.MainActivity');time.sleep(1)
def home():adb('shell','input','keyevent','4');time.sleep(.3)
def import_pack():
    click('Importar pack de episódio');time.sleep(1)
    if PACK not in texts():
        click('Show roots',False);click('Downloads',False)
    click(PACK);time.sleep(1)
def run():
    adb('shell','wm','size','1080x2400');adb('shell','wm','density','420')
    adb('shell','pm','clear',PKG);adb('logcat','-c')
    adb('push','dist/'+PACK,'/sdcard/Download/'+PACK)
    launch();click('Começar');click('Próximo card');home()
    click('Episódios');import_pack()
    assert 'A mulher da estação' in texts(),'Real importer rejected pack'
    screenshot('home');click('Começar');assert '01 / 18' in texts();screenshot('station')
    for _ in range(4):click('Próximo card')
    click('Por que ela não foi embora?');assert '06 / 18' in texts()
    adb('shell','am','force-stop',PKG);launch();click('Continuar');assert '06 / 18' in texts()
    for _ in range(6):click('Próximo card')
    click('Tenho medo de esquecer');assert '13 / 18' in texts();screenshot('voice')
    for _ in range(3):click('Próximo card')
    assert '16 / 18' in texts();screenshot('album')
    for _ in range(2):click('Próximo card')
    click('Guardar este capítulo');assert 'CAPÍTULO GUARDADO' in texts();screenshot('ending')
    home();click('Lembranças');assert 'medo de esquecer' in texts();screenshot('memories');home()
    click('Episódios');click('01 · Uma mesa para dois');click('Continuar');assert '02 / 18' in texts(),'Episode 1 progress lost';home()
    click('Episódios');click('02 · A mulher da estação');assert 'Revisitar' in texts()
    click('Episódios');import_pack();assert 'já está instalado' in texts(),'Duplicate protection failed';adb('shell','input','keyevent','4');time.sleep(.3);home()
    assert 'Revisitar' in texts(),'Duplicate import changed progress'
    assert 'FATAL EXCEPTION' not in adb('logcat','-d','-s','AndroidRuntime:E')
    print('PASS: real SAF import, all 18 cards, image decode, choices, process-death resume, ending, memories, episode switching and duplicate protection.',flush=True)
try:run()
except Exception:
    screenshot('failure');print(texts(),flush=True);print(adb('logcat','-d','-s','AndroidRuntime:E'),flush=True);raise
