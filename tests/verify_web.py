"""Render and exercise the actual R3F production build; no generated images in these checks."""
from pathlib import Path
import json,subprocess,time,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence';E.mkdir(exist_ok=True)
BASE=os.environ.get('DG_TEST_URL','http://127.0.0.1:5173')
server=subprocess.Popen(['python','-m','http.server','5173','--bind','127.0.0.1','--directory',str(ROOT/'dist')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
report={'rooms':[],'assets':[],'errors':[],'mobile':None,'tests':[]}
time.sleep(.7)
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
  page=browser.new_page(viewport={'width':1440,'height':1160},device_scale_factor=1)
  page.on('pageerror',lambda e:report['errors'].append(str(e)))
  def open_page(query):
   page.goto(BASE+'/?'+query,wait_until='networkidle',timeout=90000)
   page.wait_for_function('Number(document.documentElement.dataset.meshes)>4',timeout=120000)
   page.wait_for_timeout(1800)
  for room in ['Research','Lobby','Meeting','Corridor']:
   open_page('room='+room)
   page.screenshot(path=str(E/f'{room}_browser.png'))
   page.locator('canvas').screenshot(path=str(E/f'{room}_render.png'))
   report['rooms'].append({'room':room,'diagnostics':page.evaluate('({...document.documentElement.dataset})')})
  open_page('room=Research&fx=on&reflections=on')
  page.screenshot(path=str(E/'Research_effects_browser.png'))
  page.locator('canvas').screenshot(path=str(E/'Research_effects_render.png'))
  # Genuine interactions, not just a successful server response.
  page.get_by_label('Wireframe',exact=True).check();page.wait_for_timeout(400)
  assert page.get_by_label('Wireframe',exact=True).is_checked();page.get_by_label('Wireframe',exact=True).uncheck();report['tests'].append('wireframe toggle')
  page.get_by_label('Glass',exact=True).uncheck();assert not page.get_by_label('Glass',exact=True).is_checked();page.get_by_label('Glass',exact=True).check();report['tests'].append('glass toggle')
  page.get_by_role('button',name='Inspection',exact=True).click();report['tests'].append('inspection lighting')
  page.get_by_role('button',name='↗ Reset view').click();report['tests'].append('camera reset')
  for asset in ['WideGlassBay','EntrancePortal','ReceptionDesk','Workbench','OfficeChair','ConferenceTable','Sofa','ServerRack','MonitorWall','Planter']:
   open_page('asset='+asset)
   page.locator('canvas').screenshot(path=str(E/f'{asset}_render.png'))
   report['assets'].append({'asset':asset,'diagnostics':page.evaluate('({...document.documentElement.dataset})')})
  with page.expect_download() as info:page.get_by_role('button',name='↓ Export selected piece GLB').click()
  file=info.value;report['tests'].append('GLB download: '+file.suggested_filename)
  page.close()
  phone=browser.new_page(viewport={'width':412,'height':915},device_scale_factor=1,is_mobile=True,has_touch=True)
  phone.on('pageerror',lambda e:report['errors'].append(str(e)))
  phone.goto(BASE+'/?room=Lobby',wait_until='networkidle',timeout=90000);phone.wait_for_function('Number(document.documentElement.dataset.meshes)>4',timeout=120000);phone.wait_for_timeout(1400)
  phone.screenshot(path=str(E/'Lobby_mobile.png'))
  phone.get_by_role('button',name='Show controls').click();assert phone.locator('aside').is_visible();report['tests'].append('mobile controls')
  report['mobile']={'viewport':[412,915],'diagnostics':phone.evaluate('({...document.documentElement.dataset})'),'horizontalOverflow':phone.evaluate('document.documentElement.scrollWidth>window.innerWidth')}
  browser.close()
finally:
 server.terminate();(E/'verification.json').write_text(json.dumps(report,indent=2))
if report['errors']:raise RuntimeError(report['errors'])
print(json.dumps(report,indent=2))
