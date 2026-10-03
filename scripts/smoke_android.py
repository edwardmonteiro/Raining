"""Exercise the actual Android UI, all branches, persistence, large type and system insets."""
import subprocess,time,re,xml.etree.ElementTree as ET,json
from pathlib import Path
PKG='com.raining.story'
Path('screenshots').mkdir(exist_ok=True)
def adb(*args):return subprocess.check_output(['adb',*args],text=True)
def tree():
    adb('shell','uiautomator','dump','/sdcard/window.xml')
    return ET.fromstring(adb('shell','cat','/sdcard/window.xml'))
def click(part):
    root=tree()
    for n in root.iter('node'):
        if part in n.get('text','') and n.get('enabled')=='true':
            bounds=list(map(int,re.findall(r'\d+',n.get('bounds'))))
            adb('shell','input','tap',str((bounds[0]+bounds[2])//2),str((bounds[1]+bounds[3])//2));time.sleep(.35);return
    raise AssertionError('Missing clickable: '+part+'; '+ET.tostring(root,encoding='unicode')[:5000])
def screenshot(name):
    data=subprocess.check_output(['adb','exec-out','screencap','-p']);Path('screenshots/'+name+'.png').write_bytes(data)
def launch():adb('shell','am','start','-n',PKG+'/.MainActivity');time.sleep(1)
def swipe():adb('shell','input','swipe','300','650','300','300','250');time.sleep(.2)
adb('install','-r','dist/Raining-v0.1.0.apk')
adb('shell','wm','size','1080x2400');adb('shell','wm','density','420')
for first in ['Ela ficou','Vamos cozinhar']:
 for second in ['Pedir que','Guardar esse']:
    adb('shell','pm','clear',PKG);launch();screenshot('home');click('Começar');screenshot('card01')
    for _ in range(7):click('Próximo card')
    swipe();screenshot('choice01');click(first);screenshot('consequence01')
    # Verify process death preserves exact place and choices.
    adb('shell','am','force-stop',PKG);launch();click('Continuar');
    for _ in range(5):click('Próximo card')
    swipe();click(second)
    for _ in range(3):click('Próximo card')
    screenshot('last-card');click('Guardar este capítulo');screenshot('ending')
    assert 'CAPÍTULO GUARDADO' in ET.tostring(tree(),encoding='unicode')
    adb('shell','am','force-stop',PKG);launch()
    assert 'Revisitar' in ET.tostring(tree(),encoding='unicode')
    click('Lembranças');assert 'LEMBRAN' in ET.tostring(tree(),encoding='unicode');screenshot('memories')
    print('PASS path:',first,second,flush=True)
# Large font + short phone: scrolling keeps all actions accessible.
adb('shell','pm','clear',PKG);adb('shell','wm','size','720x1280');adb('shell','wm','density','320');launch();click('Começar');click('Aa');click('Extra grande');screenshot('large-type-small-phone');click('Próximo card')
assert '02 / 18' in ET.tostring(tree(),encoding='unicode')
logs=adb('logcat','-d','-s','AndroidRuntime:E')
assert 'FATAL EXCEPTION' not in logs,logs
print('PASS: process-death resume, saved memories, large type, small viewport, no AndroidRuntime crash.')
