"""Original Digital Gnosis kit. Deterministic textured meshes, meters, Y-up.
Mesh geometry and surface artwork are constructed here, not inferred at runtime.
"""
from pathlib import Path
from collections import defaultdict
import math,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import zoom,gaussian_filter
import trimesh as tm
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public/models';TEX=ROOT/'public/textures'
OUT.mkdir(parents=True,exist_ok=True);TEX.mkdir(parents=True,exist_ok=True)
FONT_CANDIDATES={
 'regular':['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf'],
 'bold':['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf'],
 'mono':['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf','/usr/share/fonts/dejavu-sans-fonts/DejaVuSansMono.ttf'],
}
def font(n,bold=False,mono=False):
 key='mono' if mono else 'bold' if bold else 'regular'
 for path in FONT_CANDIDATES[key]:
  if Path(path).exists():return ImageFont.truetype(path,n)
 try:return ImageFont.load_default(size=n)
 except TypeError:return ImageFont.load_default()
def rgb(h):return tuple(int(h[i:i+2],16) for i in (0,2,4))
def noise(n=512,seed=13):
 rng=np.random.default_rng(seed);result=np.zeros((n,n))
 for size,w in [(4,1),(8,.6),(16,.32),(32,.17),(64,.09),(128,.035)]:
  result+=zoom(rng.random((size,size)),n/size,order=3,mode='wrap')[:n,:n]*w
 return (result-result.mean())/(result.std()+1e-7)
MATS={}
def mat(name,color,metal=0,rough=.5,texture=None,normal=None,alpha=255,emissive=None,double=False):
 m=PBRMaterial(name=name,baseColorFactor=[*rgb(color),alpha],metallicFactor=metal,roughnessFactor=rough,alphaMode='BLEND' if alpha<255 else 'OPAQUE',doubleSided=double,baseColorTexture=texture,normalTexture=normal,emissiveFactor=np.clip(emissive,0,1) if emissive is not None else None)
 MATS[name]=m;return m
def surface(name,base,kind,rough=.5,metal=0,n=512):
 a=noise(n,hashlib.sha1(name.encode()).digest()[0]);rng=np.random.default_rng(82);y,x=np.mgrid[:n,:n]
 if kind=='stone':
  a=a*.021+rng.normal(0,.007,(n,n));a+=np.exp(-np.abs(np.sin(x*.012+y*.007+noise(n,35)*.28))*60)*.018
 elif kind=='marble':
  a=a*.012;v=np.sin(x*.009+y*.018+noise(n,43)*.45);a+=np.exp(-np.abs(v)*65)*.13
 elif kind=='leather':a=gaussian_filter(rng.normal(0,1,(n,n)),.65)*.025+a*.006
 elif kind=='rug':a=a*.024+(((x%4)<2).astype(float)-.5)*.035+(((y%4)<2).astype(float)-.5)*.035
 else:a=a*.009+rng.normal(0,.003,(n,n))
 ar=np.clip(np.array(rgb(base))[None,None,:]/255+a[:,:,None],0,1);im=Image.fromarray((ar*255).astype('uint8'));im.save(TEX/f'{name}_color.jpg',quality=92)
 gy,gx=np.gradient(a);normals=np.stack([-gx*3,-gy*3,np.ones_like(gx)],-1);normals/=np.linalg.norm(normals,axis=-1,keepdims=True)
 nm=Image.fromarray(((normals*.5+.5)*255).astype('uint8'));nm.save(TEX/f'{name}_normal.png')
 m=mat(name,'ffffff',metal,rough,im,nm);orm=np.ones((n,n,3),np.uint8)*255;orm[:,:,1]=(np.clip(rough+a*.6,.08,.99)*255).astype('uint8');orm[:,:,2]=int(metal*255)
 m.metallicRoughnessTexture=Image.fromarray(orm);m.roughnessFactor=1;m.metallicFactor=1
 return m
STEEL=surface('Powdercoat','303638','metal',.38,.40)
EDGE=mat('BlackenedSteel','171e21',.58,.32)
CHROME=mat('BrushedHardware','8b9596',.85,.26)
STONE=surface('DarkConcrete','5d5d55','stone',.31,.10,1024)
MARBLE=surface('BlackMarble','292d2d','marble',.24,.12,1024)
LEATHER=surface('BlackLeather','252829','leather',.50,0)
FABRIC=surface('GraphiteWoven','48473f','rug',.95,0)
RUBBER=mat('Rubber','111716',0,.83)
DESK=surface('GraphiteLaminate','767770','metal',.38,.08)
PAPER=mat('WarmPaper','d6cdbb',0,.85);BRASS=mat('AgedBrass','897049',.75,.4)
GLASS=mat('SmokedArchitecturalGlass','bbc7bf',.02,.08,alpha=31,double=True)
GLASS_DARK=mat('CabinetGlass','49605a',.06,.14,alpha=82,double=True)
GREEN=mat('DGGreen','40d6a4',.1,.3,emissive=[.11,1,.58])
CYAN=mat('DataCyan','64dceb',0,.2,emissive=[.10,.9,1])
MAGENTA=mat('SignalMagenta','bd349e',0,.3,emissive=[1,.035,.62])
WARM=mat('WarmWhiteDiffuser','ffddaa',0,.3,emissive=[1,.80,.55])
LEAVES=[mat(f'Foliage{i}',c,0,.85,double=True) for i,c in enumerate(['344a2d','536a3b','6b7a45','3e5832'])]
BARK=mat('BranchBark','615338',0,.9);SOIL=surface('Soil','171914','stone',.95,0,256)

def screen_image(kind='terminal',width=1024,height=576):
 im=Image.new('RGB',(width,height),'#071117');d=ImageDraw.Draw(im);rng=np.random.default_rng(sum(map(ord,kind)))
 accent='#42d9c0';cyan='#69d9e8';white='#dde9e8';muted='#789698'
 d.rounded_rectangle((12,12,width-12,height-12),10,outline='#22434c',width=2);d.text((35,25),'dg_',font=font(30,True),fill=accent);d.text((110,31),'DIGITAL GNOSIS / '+kind.upper(),font=font(17,mono=True),fill=white);d.line((30,73,width-30,73),fill='#294049',width=2)
 if kind=='signal':
  d.rectangle((20,20,width-20,height-20),fill='#481235')
  for k in range(240):
   xx=int(rng.integers(20,width-20));yy=int(rng.integers(20,height-20));d.rectangle((xx,yy,xx+int(rng.integers(4,45)),yy+2),fill=(int(rng.integers(65,110)),20,int(rng.integers(50,90))))
  for txt,xy,size,col in [('SIGNAL',(55,75),105,'#f098da'),('REVIEW READY',(58,225),42,'#f7d8ec'),('CREATIVE / 04',(60,350),24,'#b665a0'),('DEMONSTRATION',(60,425),18,'#da98c6')]:d.text(xy,txt,font=font(size,mono=size<60),fill=col)
 elif kind=='map':
  for xx in range(35,width-30,48):d.line((xx,95,xx,height-55),fill='#163b46')
  for yy in range(95,height-55,40):d.line((35,yy,width-35,yy),fill='#163b46')
  polys=[[(.08,.24),(.18,.15),(.29,.18),(.34,.25),(.26,.35),(.23,.39),(.17,.36),(.13,.29)],[(.25,.41),(.32,.46),(.33,.59),(.29,.76),(.24,.62)],[(.45,.25),(.50,.19),(.61,.20),(.65,.15),(.8,.22),(.93,.32),(.83,.45),(.74,.42),(.64,.36),(.6,.46),(.54,.4),(.48,.33)],[(.47,.37),(.56,.40),(.59,.54),(.54,.7),(.48,.62),(.44,.47)],[(.77,.66),(.87,.63),(.91,.73),(.82,.76)]]
  for poly in polys:d.polygon([(int(x*width),int(y*(height-90)+70)) for x,y in poly],fill='#357c8d',outline='#71c0c5')
  for k in range(20):
   xx=int(rng.integers(100,width-100));yy=int(rng.integers(170,height-110));d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=accent)
   if k<6:d.ellipse((xx-13,yy-13,xx+13,yy+13),outline='#529292',width=1)
  d.text((35,height-45),'NETWORK TOPOLOGY    /    STUDIO DEMO',font=font(15,mono=True),fill=muted)
 elif kind=='metrics':
  d.text((40,100),'PROJECT / ORION',font=font(27,True),fill=white)
  for k,(label,value) in enumerate([('ITERATIONS','024'),('ARTIFACTS','018'),('IN REVIEW','003')]):
   xx=40+k*310;d.text((xx,155),label,font=font(17,mono=True),fill=muted);d.text((xx,194),value,font=font(58),fill=accent)
  for k in range(30):
   xx=45+k*31;hh=int(40+abs(math.sin(k*.4))*120+k*2);d.rectangle((xx,height-75-hh,xx+18,height-75),fill='#419a96' if k%3 else '#77cfc4')
  d.text((40,height-45),'ILLUSTRATIVE DATA / NOT CONNECTED',font=font(16,mono=True),fill=muted)
 elif kind=='blueprint':
  for xx in range(30,width-30,40):d.line((xx,90,xx,height-35),fill='#204859')
  for yy in range(90,height-30,40):d.line((30,yy,width-30,yy),fill='#204859')
  for k in range(6):
   xx=160+k*72;yy=155+k*12;d.polygon([(xx,yy),(xx+280,yy+65),(xx+280,yy+205),(xx,yy+140)],outline='#56a8ba',width=2)
  d.text((35,103),'VOLUME / 03',font=font(25,mono=True),fill=cyan);d.text((35,height-49),'RECONSTRUCTION / REFERENCE STUDY',font=font(18,mono=True),fill=muted)
 else:
  d.rectangle((30,92,215,height-32),fill='#0a1b23')
  for k,label in enumerate(['RESEARCH','EVIDENCE','ARTIFACTS','REVIEW','DELIVERY']):d.text((48,120+k*61),label,font=font(17,mono=True),fill=accent if k==0 else muted)
  lines=['// STUDIO WORLD / RESEARCH','const workspace = {','  project: "Digital Gnosis",','  process: "research",','  evidence: [],','  status: "demonstration"','};','','function inspect(artifact) {','  return {','    source: artifact.origin,','    review: "pending",','    lineage: artifact.history','  };','}']
  for k,line in enumerate(lines):d.text((235,110+k*26),f'{k+1:02}',font=font(16,mono=True),fill='#36505e');d.text((280,110+k*26),line,font=font(18,mono=True),fill=cyan if k%3==0 else '#a7bbb9')
 im.save(TEX/f'screen_{kind}.png');return im
SCREEN={}
for kind in ['terminal','map','metrics','blueprint','signal']:
 tex=screen_image(kind);m=mat('Screen_'+kind,'ffffff',0,.65,tex,emissive=[.5,.5,.5]);m.emissiveTexture=tex;SCREEN[kind]=m

def textmat(name,lines,w=1024,h=1024,accent=False,transparent=False):
 im=Image.new('RGBA',(w,h),(0,0,0,0) if transparent else (16,22,24,255));d=ImageDraw.Draw(im)
 for txt,x,y,size,color in lines:d.text((x,y),txt,font=font(size,txt=='DG',mono=txt not in ['DG','Digital Gnosis.']),fill=color)
 if not transparent:d.rectangle((4,4,w-5,h-5),outline=(54,62,64,255),width=4)
 im.save(TEX/f'{name}.png');m=mat(name,'ffffff',0,.6,im,double=True)
 if transparent:m.alphaMode='BLEND'
 if accent:m.emissiveTexture=im;m.emissiveFactor=np.array([.25,.4,.3])
 return m
LOGO=textmat('DGIdentity',[('DG',100,75,235,'#62d8b3'),('RESEARCH',110,435,56,'#bac8c2'),('INTO',110,530,56,'#bac8c2'),('REALITY',110,625,56,'#bac8c2')],768,1024,True)
SLOGAN=textmat('Slogan',[('IDEAS',80,100,56,'#a8b5b1'),('AGENTS',80,215,56,'#a8b5b1'),('SYSTEMS',80,330,56,'#a8b5b1'),('OUTCOMES',80,445,56,'#a8b5b1')],600,760)
WORDMARK=textmat('Wordmark',[('Digital Gnosis.',15,20,65,'#dee2dc')],660,120,True,True)
GLASSLOGO=textmat('GlassWordmark',[('DIGITAL GNOSIS',30,32,50,'#c5d7d2')],650,120,False,True)
FLOORLABEL=textmat('FloorMark',[('01 / RESEARCH',15,10,58,'#b2b9af')],750,110,False,True)
KEYS_IMG=Image.new('RGB',(600,220),'#161c1e');kd=ImageDraw.Draw(KEYS_IMG)
for row in range(5):
 for col in range(16):
  xx=9+col*36;yy=10+row*39;kd.rounded_rectangle((xx,yy,xx+28,yy+30),3,fill='#444d50',outline='#687375');kd.text((xx+7,yy+4),chr(65+(col+row*9)%26),font=font(10),fill='#b4c4c1')
KEYS=mat('KeyboardKeys','ffffff',0,.6,KEYS_IMG)

class Build:
 def __init__(self,name):self.name=name;self.parts=[]
 def add(self,mesh,material,name='part'):
  if not isinstance(mesh.visual,TextureVisuals):
   v=mesh.vertices[mesh.faces].reshape(-1,3);f=np.arange(len(v)).reshape(-1,3);n=np.repeat(mesh.face_normals,3,axis=0);axes=np.argmax(np.abs(n),axis=1);uv=np.zeros((len(v),2))
   uv[axes==0]=v[axes==0][:,[2,1]];uv[axes==1]=v[axes==1][:,[0,2]];uv[axes==2]=v[axes==2][:,[0,1]]
   mesh=tm.Trimesh(vertices=v,faces=f,process=False);mesh.visual=TextureVisuals(uv=uv,material=material)
  else:mesh.visual.material=material
  self.parts.append((mesh,material,name));return mesh
 def box(self,size,p=(0,0,0),material=STEEL,b=.008,name='body',rot=None):
  ext=np.array(size,float);b=min(b,float(ext.min())*.3)
  if b>0:
   pts=[]
   for sx in [-1,1]:
    for sy in [-1,1]:
     for sz in [-1,1]:
      signs=np.array([sx,sy,sz]);v=signs*(ext/2-b)
      for axis in range(3):q=v.copy();q[axis]+=signs[axis]*b;pts.append(q)
   m=tm.convex.convex_hull(np.array(pts))
  else:m=tm.creation.box(extents=ext)
  if rot is not None:m.apply_transform(tm.transformations.euler_matrix(*rot))
  m.apply_translation(p);return self.add(m,material,name)
 def cyl(self,r,h,p=(0,0,0),material=STEEL,axis=(0,1,0),sections=14,name='tube'):
  m=tm.creation.cylinder(radius=r,height=h,sections=sections);m.apply_transform(tm.geometry.align_vectors([0,0,1],axis));m.apply_translation(p);return self.add(m,material,name)
 def line(self,a,b,r=.02,material=EDGE,sections=10):
  a,b=np.array(a),np.array(b);v=b-a;return self.cyl(r,np.linalg.norm(v),(a+b)/2,material,v,sections)
 def pipe(self,pts,r=.025,material=EDGE):
  for a,b in zip(pts[:-1],pts[1:]):self.line(a,b,r,material)
 def torus(self,R,r,p,material=STEEL,axis=(0,1,0)):
  m=tm.creation.torus(major_radius=R,minor_radius=r,major_sections=16,minor_sections=6);m.apply_transform(tm.geometry.align_vectors([0,0,1],axis));m.apply_translation(p);return self.add(m,material)
 def cushion(self,size,p,material=LEATHER):
  u=np.linspace(-math.pi/2,math.pi/2,11);v=np.linspace(-math.pi,math.pi,21);U,V=np.meshgrid(u,v,indexing='ij');sp=lambda x,e:np.sign(x)*np.abs(x)**e
  a=np.stack([sp(np.cos(U),.23)*sp(np.cos(V),.23),sp(np.sin(U),.3),sp(np.cos(U),.23)*sp(np.sin(V),.23)],-1).reshape(-1,3)*np.array(size)/2;faces=[]
  for i in range(10):
   for j in range(20):k=i*21+j;faces.extend([[k,k+21,k+1],[k+1,k+21,k+22]])
  m=tm.Trimesh(a+np.array(p),np.array(faces),process=False);return self.add(m,material,'upholstery')
 def plane(self,size,p,material,rot=None,name='surface'):
  w,h=size;m=tm.Trimesh([[-w/2,-h/2,0],[w/2,-h/2,0],[w/2,h/2,0],[-w/2,h/2,0]],[[0,1,2],[0,2,3]],process=False);m.visual=TextureVisuals(uv=[[0,0],[1,0],[1,1],[0,1]],material=material)
  if rot is not None:m.apply_transform(tm.transformations.euler_matrix(*rot))
  m.apply_translation(p);return self.add(m,material,name)
 def into(self,other,p=(0,0,0),ry=0):
  t=tm.transformations.rotation_matrix(ry,[0,1,0]);t[:3,3]=p
  for mesh,ma,n in other.parts:m=mesh.copy();m.apply_transform(t);self.parts.append((m,ma,n))
 def scene(self):
  s=tm.Scene();buckets=defaultdict(list)
  for m,ma,n in self.parts:buckets[(ma.name,n if n.startswith('screen_') else 'mesh')].append(m)
  for (mn,part),ms in buckets.items():
   v=[];f=[];uv=[];offset=0
   for m in ms:v.append(m.vertices);f.append(m.faces+offset);uv.append(m.visual.uv);offset+=len(m.vertices)
   mesh=tm.Trimesh(np.vstack(v),np.vstack(f),process=False);mesh.visual=TextureVisuals(uv=np.vstack(uv),material=MATS[mn]);s.add_geometry(mesh,node_name=f'{self.name}__{mn}__{part}',geom_name=f'{mn}__{part}')
  return s
ASSETS={}
def register(b,category):ASSETS[b.name]=(b,category);return b
