from pathlib import Path
import base64,json,re,mimetypes
ROOT=Path(__file__).resolve().parents[1];dist=ROOT/'dist'
files={}
for d in ['models','textures']:
 for p in (dist/d).iterdir():
  if p.is_file():
   mime='model/gltf-binary' if p.suffix=='.glb' else mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
   files[p.relative_to(dist).as_posix()]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='\n'.join(p.read_text() for p in (dist/'assets').glob('*.css'))
js='\n'.join(p.read_text() for p in (dist/'assets').glob('*.js')).replace('</script','<\\/script')
html='<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Digital Gnosis / Studio Kit</title><style>'+css+'</style></head><body><div id="root"></div><script>window.__DG_ASSETS__='+json.dumps(files,separators=(',',':'))+';</script><script type="module">'+js+'</script></body></html>'
(ROOT/'DG_Studio_Preview.html').write_text(html)
print('Self-contained preview',len(html),'bytes',len(files),'embedded assets. Zero CDN requests.')
