"""Real Chromium smoke test. Captures are evidence, not automatic art approval.
Install playwright (+ Chromium), build Vite, then run this script.
On a desktop with system Chromium requiring X11, use xvfb-run -a.
All application resources are embedded; no external web requests are needed.
"""
import base64, json, mimetypes, os, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'; OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
files={}
for folder in ['models','textures']:
 for path in (DIST/folder).iterdir():
  if not path.is_file() or path.name.endswith('Room.glb'):continue
  mime='model/gltf-binary' if path.suffix=='.glb' else mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
  files[path.relative_to(DIST).as_posix()]='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
css='\n'.join(p.read_text() for p in (DIST/'assets').glob('*.css'))
js='\n'.join(p.read_text() for p in (DIST/'assets').glob('*.js')).replace('</script','<\\/script')
html='<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>'+css+'</style></head><body><div id="root"></div><script>window.__DG_ASSETS__='+json.dumps(files)+';</script><script type="module">'+js.replace('location.search',repr('?room=Lobby&perf=1'))+'</script></body></html>'
report={'environment':'Chromium software renderer, mobile-sized viewport; NOT phone GPU FPS','rooms':[],'tests':[],'errors':[]}
with sync_playwright() as p:
 executable=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
 browser=p.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':412,'height':915},device_scale_factor=2,is_mobile=True,has_touch=True)
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.set_content(html,wait_until='load',timeout=90000);page.wait_for_timeout(800)
 try:
  for room in ['Lobby','Research','Meeting','Corridor']:
   if room!='Lobby':
    page.get_by_role('button',name='Show controls').click()
    page.locator('.room-list button').filter(has_text=room).click()
   page.wait_for_timeout(1500)
   page.evaluate('window.__invalidate()');page.wait_for_timeout(200)
   metrics=page.evaluate('window.__DG_METRICS__')
   aa=page.evaluate('window.__gl.getContext().getContextAttributes().antialias')
   assert aa, 'Antialiasing must not be disabled'
   assert metrics and metrics['textures']<70
   page.screenshot(path=str(OUT/f'{room.lower()}-mobile.png'))
   report['rooms'].append({'room':room,**metrics,'antialias':aa})
  # Exercise the UI, rather than only taking successful-load screenshots.
  page.get_by_role('button',name='Show controls').click()
  for label in ['Glass','Wireframe','Scale figures','Frontage']:
   toggle=page.get_by_label(label,exact=True);initial=toggle.is_checked();toggle.set_checked(not initial);page.wait_for_timeout(120);toggle.set_checked(initial)
   report['tests'].append(label+' toggle')
  page.get_by_role('button',name='High',exact=True).click();page.wait_for_timeout(600)
  assert page.evaluate('window.__gl.getPixelRatio()')==2
  report['tests'].append('High resolves at DPR 2')
  page.get_by_role('button',name='Balanced',exact=True).click()
  page.get_by_role('button',name='Show controls').click()
  page.get_by_role('button',name='↗ Reset view').click();report['tests'].append('camera reset')
  page.get_by_role('button',name='Components',exact=True).click()
  page.locator('.asset-list button').filter(has_text='ReceptionDesk').click()
  page.wait_for_timeout(800)
  page.screenshot(path=str(OUT/'reception-component.png'))
  report['tests'].append('standalone component mode')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  report['tests'].append('no mobile horizontal overflow')
  page.set_viewport_size({'width':1280,'height':960})
  page.get_by_role('button',name='Room studies',exact=True).click()
  page.locator('.room-list button').filter(has_text='Lobby').click();page.wait_for_timeout(800)
  page.screenshot(path=str(OUT/'lobby-desktop.png'))
  # Project a known world coordinate to click the instanced reception counter.
  xy=page.evaluate('(()=>{const p=window.__camera.position.clone().set(-.55,.9,-.39).project(window.__camera),r=document.querySelector("canvas").getBoundingClientRect();return {x:r.x+(p.x+1)*r.width/2,y:r.y+(1-p.y)*r.height/2}})()')
  page.mouse.click(xy['x'],xy['y']);page.wait_for_timeout(100)
  selected=page.locator('.inspector h3').inner_text();assert selected=='ReceptionDesk',selected
  report['tests'].append('instanced component picking retains ReceptionDesk identity')
  # Check the export target without saving a file (browser policies vary).
  href=page.evaluate('(()=>{let h;const old=HTMLAnchorElement.prototype.click;HTMLAnchorElement.prototype.click=function(){h=this.download};document.querySelector(".download").click();HTMLAnchorElement.prototype.click=old;return h})()')
  assert href=='ReceptionDesk.glb';report['tests'].append('selected raw GLB export target preserved')
 finally:
  browser.close();(OUT/'north-star-verification.json').write_text(json.dumps(report,indent=2))
if report['errors']:raise RuntimeError(report['errors'])
print(json.dumps(report,indent=2))
