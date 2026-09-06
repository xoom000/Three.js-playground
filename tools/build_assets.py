from geometry import *
# STRUCTURAL COMPONENTS
b=Build('FloorTile');b.box((1.196,.11,1.196),(0,-.055,0),STONE,.006);register(b,'architecture')
b=Build('WallPanel');b.box((1.2,3.2,.18),(0,1.6,0),EDGE);b.box((1.16,2.9,.05),(0,1.59,.106),STEEL,.006)
b.box((1.2,.13,.24),(0,.065,.02),EDGE);b.box((1.2,.15,.24),(0,3.125,.02),EDGE);register(b,'architecture')
b=Build('StructuralColumn');b.box((.27,3.2,.27),(0,1.6,0),EDGE,.013);b.box((.19,2.98,.016),(0,1.6,.145),STEEL,.003)
for y in [.16,3.04]:b.box((.30,.055,.3),(0,y,0),STEEL,.008)
register(b,'architecture')
def glassbay(w=1.2):
 b=Build('GlassBay')
 for x in [-w/2+.033,w/2-.033]:b.box((.067,3.2,.12),(x,1.6,0),EDGE,.004);b.box((.016,3.04,.025),(x,1.59,.071),STEEL,.002)
 for y in [.048,3.15]:b.box((w,.085,.12),(0,y,0),EDGE,.004)
 b.plane((w-.12,3.00),(0,1.6,0),GLASS,name='glass_pane');return b
register(glassbay(),'architecture')
b=Build('GlassCorner');b.into(glassbay(),(.6,0,0));b.into(glassbay(),(0,0,.6),math.pi/2);register(b,'architecture')
def door(w=1.2,two=False):
 b=Build('DoubleGlassDoor' if two else 'GlassDoor');fr=.075
 for x in [-(w-fr)/2,(w-fr)/2]:b.box((fr,3.2,.15),(x,1.6,0),EDGE,.005)
 b.box((w,.15,.15),(0,3.125,0),EDGE,.008);leaves=2 if two else 1;leafw=(w-2*fr)/leaves-.015
 for i in range(leaves):
  cx=0 if leaves==1 else (i-.5)*(w-2*fr)/2
  for x in [cx-(leafw-.04)/2,cx+(leafw-.04)/2]:b.box((.04,3.02,.065),(x,1.52,0),EDGE,.003)
  for yy in [.045,3.]:b.box((leafw,.05,.065),(cx,yy,0),EDGE,.003)
  b.plane((leafw-.08,2.91),(cx,1.52,.004),GLASS,name='glass_leaf');hx=cx+leafw*.32*(-1 if i else 1)
  for z in [-.065,.065]:
   b.cyl(.014,.70,(hx,1.28,z),CHROME,sections=10)
   for yy in [.99,1.57]:b.line((hx,yy,0),(hx,yy,z),.01,CHROME)
  for yy in [.36,2.65]:b.box((.046,.1,.1),(cx-leafw/2,yy,0),CHROME,.004)
 b.box((w,.012,.16),(0,.006,0),CHROME,.003);return b
register(door(),'architecture');register(door(2.2,True),'architecture')
b=Build('CeilingBeam');b.box((2.4,.21,.24),(0,0,0),EDGE,.009);b.box((2.34,.04,.265),(0,-.073,0),STEEL,.003);register(b,'architecture')
b=Build('PipeRun')
for r,y in [(.045,0),(.025,.15),(.017,.25)]:
 b.line((-.6,y,0),(.6,y,0),r,EDGE,14)
 for xx in [-.42,.35]:b.cyl(r*1.35,.065,(xx,y,0),STEEL,(1,0,0),14)
for xx in [-.40,.36]:b.box((.04,.42,.04),(xx,.1,-.055),CHROME,.003)
register(b,'architecture')
b=Build('PipeElbow')
for r,off in [(.045,0),(.025,.16),(.017,.28)]:
 pts=[(.26*math.sin(t),off,.26*(1-math.cos(t))) for t in np.linspace(0,math.pi/2,14)];b.pipe(pts,r,EDGE);b.cyl(r*1.35,.05,pts[0],STEEL,(1,0,0));b.cyl(r*1.35,.05,pts[-1],STEEL,(0,0,1))
register(b,'architecture')
b=Build('CableTray')
for zz in [-.18,.18]:b.box((2.4,.075,.025),(0,0,zz),STEEL,.003)
for xx in np.linspace(-1.17,1.17,16):b.box((.035,.025,.36),(xx,-.02,0),STEEL,.003)
for i in range(6):b.line((-1.2,.026,-.12+i*.045),(1.2,.026,-.12+i*.045),.011,RUBBER)
register(b,'architecture')
b=Build('LinearLight');b.box((1.8,.055,.09),(0,0,0),EDGE,.008);b.box((1.71,.014,.055),(0,-.032,0),WARM,.003);b.box((1.71,.026,.015),(0,0,.049),WARM,.003)
for xx in [-.7,.7]:b.line((xx,.02,0),(xx,.20,0),.004,CHROME,6)
register(b,'architecture')
b=Build('WallSconce');b.box((.105,.72,.08),(0,0,0),EDGE,.008);b.box((.054,.61,.014),(0,0,.045),WARM,.007);register(b,'architecture')
b=glassbay(2.4);b.name='WideGlassBay';register(b,'architecture')
b=Build('EntrancePortal')
for x in [-1.24,1.24]:b.box((.27,3.24,.36),(x,1.62,0),EDGE,.012);b.box((.043,.78,.015),(x,1.94,.185),WARM,.004)
b.box((2.75,.25,.37),(0,3.17,0),EDGE,.01);b.box((2.20,.027,.02),(0,3.025,.19),WARM,.003);register(b,'architecture')
b=Build('FacadeHeader');b.box((2.4,.19,.22),(0,0,0),EDGE,.009);register(b,'architecture')
b=Build('FloorPlinth');b.box((1.2,.22,1.2),(0,-.22,0),EDGE,.008);register(b,'architecture')
# FURNITURE

def drawer(b,x,y,z,w=.46):b.box((w,.15,.02),(x,y,z),STEEL,.005);b.box((.13,.014,.026),(x,y+.02,z+.02),CHROME,.003)
b=Build('Workbench');b.box((2.7,.055,.90),(0,.765,0),DESK,.015);b.box((2.62,.025,.85),(0,.721,0),EDGE,.005)
for x in [-1.03,1.03]:
 b.box((.50,.69,.77),(x,.37,0),EDGE,.014);b.box((.43,.055,.71),(x,.035,0),STEEL,.004)
 for y in [.22,.39,.56]:drawer(b,x,y,.39)
b.box((1.50,.23,.04),(0,.54,-.36),EDGE,.005);b.box((1.6,.07,.06),(0,.72,-.38),EDGE,.005)
for x in [-.62,.65]:b.cyl(.032,.004,(x,.795,-.28),RUBBER)
register(b,'furniture')
b=Build('ReceptionDesk');b.box((3.60,1.02,.79),(0,.55,0),MARBLE,.018);b.box((3.72,.07,.93),(0,1.095,0),MARBLE,.018);b.box((3.42,.08,.64),(0,.065,0),EDGE,.008);b.box((3.43,.018,.70),(0,.098,.02),WARM,.003);b.box((3.3,.046,.44),(0,.765,-.48),DESK,.01);b.plane((2.15,.40),(0,.62,.405),WORDMARK,name='brand_wordmark')
for x in [-1.35,1.35]:b.box((.48,.64,.38),(x,.37,-.47),EDGE,.009)
register(b,'furniture')
b=Build('ConferenceTable');b.box((4.5,.09,1.42),(0,.79,0),MARBLE,.032)
for x in [-1.65,1.65]:b.box((.19,.71,.93),(x,.40,0),EDGE,.014);b.box((.63,.07,1.11),(x,.075,0),EDGE,.012)
b.box((4.0,.016,.043),(0,.842,0),WARM,.003)
for x in [-1.20,1.2]:b.box((.27,.018,.16),(x,.846,.05),EDGE,.004)
register(b,'furniture')
b=Build('OfficeChair')
for k in range(5):
 a=k*2*math.pi/5;end=(.30*math.cos(a),.08,.30*math.sin(a));b.line((0,.14,0),end,.022,CHROME)
 for dx in [-.018,.018]:b.cyl(.038,.018,(end[0]+dx,.045,end[2]),RUBBER,(1,0,0),12)
b.cyl(.032,.27,(0,.255,0),CHROME);b.cyl(.048,.11,(0,.39,0),RUBBER);b.box((.47,.045,.45),(0,.47,0),EDGE,.012);b.cushion((.52,.09,.48),(0,.53,0),LEATHER)
b.box((.43,.53,.052),(0,.82,-.235),EDGE,.012,rot=(-.13,0,0))
for yy in [.66,.88]:b.cushion((.45,.20,.072),(0,yy,-.205),LEATHER)
b.cushion((.29,.14,.085),(0,1.084,-.245),LEATHER)
for x in [-.29,.29]:b.line((x,.48,-.15),(x,.73,-.12),.018,CHROME);b.line((x,.73,-.12),(x,.73,.13),.018,CHROME);b.box((.07,.04,.31),(x,.765,0),LEATHER,.009)
register(b,'furniture')
b=Build('Sofa');b.box((2.55,.20,.83),(0,.22,0),EDGE,.028)
for x in [-1.10,1.10]:
 for z in [-.30,.30]:b.box((.05,.15,.05),(x,.075,z),CHROME,.009)
for xx in [-1.21,1.21]:b.cushion((.19,.61,.86),(xx,.49,0),LEATHER)
b.box((2.37,.46,.13),(0,.59,-.38),EDGE,.025)
for xx in [-.75,0,.75]:
 b.cushion((.70,.15,.65),(xx,.40,.055),LEATHER);b.cushion((.70,.34,.17),(xx,.655,-.27),LEATHER)
 for z in [-.19,.29]:b.line((xx-.30,.475,z),(xx+.30,.475,z),.0018,EDGE,6)
 b.cyl(.013,.006,(xx,.657,-.177),EDGE,(0,0,1),8)
register(b,'furniture')
b=Build('CoffeeTable');b.box((1.30,.05,.66),(0,.38,0),MARBLE,.018);b.box((1.12,.027,.51),(0,.15,0),STEEL,.008)
for x in [-.53,.53]:
 for z in [-.24,.24]:b.box((.035,.355,.035),(x,.178,z),EDGE,.004)
register(b,'furniture')
b=Build('SideCabinet');b.box((1.60,.78,.46),(0,.425,0),EDGE,.014);b.box((1.66,.045,.51),(0,.842,0),MARBLE,.01)
for x in [-.4,.4]:b.box((.77,.69,.025),(x,.44,.246),STEEL,.005);b.box((.017,.15,.027),(x+.29,.61,.269),CHROME,.003)
for x in [-.65,.65]:b.box((.045,.08,.35),(x,.04,0),STEEL,.005)
register(b,'furniture')
b=Build('Bookcase')
for x in [-.5,.5]:b.box((.035,2.25,.035),(x,1.125,.19),EDGE,.004);b.box((.035,2.25,.035),(x,1.125,-.19),EDGE,.004)
for y in [.15,.68,1.21,1.74,2.24]:b.box((1.05,.035,.44),(0,y,0),DESK,.004)
for yy in [.19,.72,1.25]:
 for i in range(8):
  hh=.23+(i%3)*.036;b.box((.05,hh,.20),(-.39+i*.074,yy+hh/2,.03),PAPER if i%4 else BRASS,.002,rot=(0,0,.025*(i%3)))
register(b,'furniture')
b=Build('UtilityCart')
for y in [.24,.67]:b.box((.82,.025,.45),(0,y,0),STEEL,.007)
for x in [-.37,.37]:
 for z in [-.19,.19]:b.box((.025,.69,.025),(x,.40,z),CHROME,.002);b.cyl(.043,.03,(x,.06,z),RUBBER,(1,0,0))
for x in [-.38,.38]:b.line((x,.69,-.20),(x,.83,-.20),.014,CHROME)
b.line((-.38,.83,-.20),(.38,.83,-.20),.014,CHROME);register(b,'furniture')
b=Build('Rug');b.box((3.3,.012,2.1),(0,.006,0),FABRIC,.004);register(b,'furniture')
# TECH EQUIPMENT
b=Build('Monitor');b.box((.65,.38,.033),(0,.40,0),EDGE,.009);b.box((.44,.24,.022),(0,.40,-.027),STEEL,.014);b.plane((.608,.334),(0,.408,.018),SCREEN['terminal'],name='screen_main');b.line((0,.08,-.03),(0,.28,-.035),.023,CHROME);b.box((.24,.018,.18),(0,.018,-.01),EDGE,.007);b.cyl(.004,.002,(.27,.225,.019),GREEN,(0,0,1),8)
for yy in [.30,.34,.38,.42,.46]:b.box((.29,.004,.005),(0,yy,-.041),RUBBER,.001)
register(b,'technology')
b=Build('Keyboard');b.box((.44,.020,.155),(0,.013,0),EDGE,.007);b.plane((.414,.143),(0,.024,0),KEYS,(-math.pi/2,0,0),name='keys');register(b,'technology')
b=Build('Mouse');b.cushion((.062,.035,.102),(0,.022,0),EDGE);b.line((0,.036,-.045),(0,.041,0),.0015,CHROME,6);register(b,'technology')
b=Build('Laptop');b.box((.37,.019,.255),(0,.015,0),STEEL,.006);b.plane((.33,.117),(0,.026,-.029),KEYS,(-math.pi/2,0,0));b.box((.11,.002,.06),(0,.026,.076),EDGE,.003);b.box((.37,.24,.013),(0,.145,-.115),EDGE,.006,rot=(-.17,0,0));b.plane((.34,.212),(0,.149,-.103),SCREEN['blueprint'],(-.17,0,0),name='screen_laptop');register(b,'technology')
b=Build('WallDisplay');b.box((1.80,1.045,.09),(0,0,0),EDGE,.012);b.box((1.31,.67,.04),(0,0,-.063),STEEL,.005);b.plane((1.728,.973),(0,0,.049),SCREEN['map'],name='screen_display');register(b,'technology')
b=Build('MonitorWall')
for x,y,w,h,kind in [(-1.48,2.39,1.82,1.05,'map'),(.48,2.60,1.82,.83,'signal'),(-1.47,1.36,1.82,.88,'blueprint'),(.11,1.56,1.28,1.07,'terminal'),(1.39,1.39,1.12,.75,'metrics'),(1.40,2.06,1.12,.49,'terminal'),(.05,.58,1.12,.61,'metrics')]:
 b.box((w,h,.085),(x,y,0),EDGE,.012);b.plane((w-.055,h-.055),(x,y,.047),SCREEN[kind],name='screen_'+kind);b.pipe([(x,y,-.06),(x,y-.12,-.10),(x+.08,.20,-.10)],.009,RUBBER)
register(b,'technology')
b=Build('ServerRack');b.box((.77,2.28,.78),(0,1.20,0),EDGE,.01)
for x in [-.355,.355]:b.box((.022,2.08,.04),(x,1.18,.408),CHROME,.002)
for i in range(13):
 y=.24+i*.149;b.box((.651,.130,.075),(0,y,.43),STEEL,.007)
 for j in range(14):b.box((.023,.067,.008),(-.23+j*.035,y,.474),RUBBER,.001)
 for x in [-.294,.289]:b.box((.011,.043,.012),(x,y,.481),GREEN,.001)
 if i%4==0:b.box((.025,.022,.012),(.248,y,.481),CYAN,.002)
for x in [-.285,.285]:
 for z in [-.285,.285]:b.box((.063,.085,.063),(x,.045,z),CHROME,.004)
b.plane((.695,2.01),(0,1.19,.49),GLASS_DARK,name='glass_server');b.box((.019,.36,.035),(.294,1.07,.512),CHROME,.004);register(b,'technology')
b=Build('BadgeReader');b.box((.10,.21,.045),(0,0,0),EDGE,.010);b.box((.061,.040,.012),(0,.056,.025),GREEN,.004);b.box((.06,.08,.008),(0,-.039,.025),STEEL,.004);register(b,'technology')
b=Build('AccessGate')
for x in [-.48,.48]:b.box((.19,1.03,.62),(x,.515,0),EDGE,.016);b.box((.20,.035,.65),(x,1.047,0),STEEL,.007);b.box((.08,.012,.22),(x,1.070,.14),GREEN,.002);b.box((.026,.64,.012),(x-.01,.66,.317),GREEN,.002)
b.plane((.73,.69),(0,.57,.02),GLASS,name='gate_glass');register(b,'technology')
b=Build('Kiosk');b.box((.52,1.60,.27),(0,.83,0),EDGE,.018);b.box((.64,.07,.47),(0,.045,0),STEEL,.01);b.plane((.43,.72),(0,1.12,.143),SCREEN['metrics'],name='screen_kiosk');b.box((.17,.06,.035),(0,.53,.15),GREEN,.004);register(b,'technology')
b=Build('Tablet');b.box((.26,.013,.18),(0,.04,0),EDGE,.005,rot=(.20,0,0));b.plane((.235,.149),(0,.05,0),SCREEN['metrics'],(-math.pi/2+.20,0,0),name='screen_tablet');register(b,'technology')
# DRESSING
b=Build('Planter');verts=[]
for yy,s in [(0,.40),(.62,.50)]:
 for x,z in [(-1,-1),(1,-1),(1,1),(-1,1)]:verts.append((x*s/2,yy,z*s/2))
faces=[[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7],[0,3,2],[0,2,1]];b.add(tm.Trimesh(verts,faces,process=False),STEEL)
for x in [-.246,.246]:b.box((.016,.022,.50),(x,.621,0),CHROME,.002)
for z in [-.246,.246]:b.box((.48,.022,.016),(0,.621,z),CHROME,.002)
b.box((.465,.017,.465),(0,.591,0),SOIL,.001);rng=np.random.default_rng(442)
for stem in range(5):
 a=stem*2.399;height=1.04+rng.uniform(-.17,.3);end=np.array([math.cos(a)*.13,.62+height,math.sin(a)*.13]);start=np.array([0,.59,0]);b.line(start,end,.007,BARK,8)
 for j in range(6):
  t=.20+j*.14;center=start*(1-t)+end*t;ang=a+j*2.4;leafend=center+np.array([math.cos(ang)*(.25+t*.06),.04,math.sin(ang)*(.25+t*.06)]);b.line(center,leafend,.003,BARK,6)
  for side in [-1,1]:
   for k in [.42,.72,1.0]:
    base=center+(leafend-center)*k;direction=np.array([math.cos(ang+side*.65),.25,math.sin(ang+side*.65)])*.14;mid=base+direction*.52+np.array([0,.025,0]);perp=np.array([-direction[2],0,direction[0]])*.19;tip=base+direction
    mm=tm.Trimesh([base,mid+perp,tip,mid-perp,mid+np.array([0,.008,0])],[[0,1,4],[1,2,4],[2,3,4],[3,0,4]],process=False);b.add(mm,LEAVES[(stem+j)%4],'leaves')
register(b,'dressing')
b=Build('DeskPlant');b.into(ASSETS['Planter'][0])
for m,_,_ in b.parts:m.apply_scale(.26)
register(b,'dressing')
b=Build('BookStack')
for i in range(3):b.box((.23-i*.016,.033,.17-i*.008),(0,.02+i*.040,0),PAPER,.002,rot=(0,i*.08,0));b.box((.238-i*.016,.004,.177-i*.008),(0,.038+i*.040,0),BRASS if i==1 else STEEL,.001,rot=(0,i*.08,0))
register(b,'dressing')
b=Build('Mug');b.cyl(.036,.088,(0,.051,0),STEEL,sections=20);b.cyl(.030,.003,(0,.096,0),RUBBER,sections=20);b.torus(.032,.006,(.035,.057,0),STEEL,(0,0,1));register(b,'dressing')
b=Build('CoffeeMachine');b.box((.32,.40,.32),(0,.22,0),CHROME,.016);b.box((.285,.30,.026),(0,.23,.17),EDGE,.008);b.box((.28,.029,.14),(0,.073,.19),CHROME,.003);b.box((.16,.07,.028),(0,.355,.19),RUBBER,.005);b.box((.042,.032,.01),(.064,.355,.209),GREEN,.001)
for x in [-.04,.04]:b.cyl(.009,.055,(x,.21,.205),CHROME)
register(b,'dressing')
b=Build('DGLogoPanel');b.box((1.48,2.20,.045),(0,0,0),EDGE,.006);b.plane((1.43,2.14),(0,0,.026),LOGO,name='brand_sign');register(b,'dressing')
b=Build('SloganPanel');b.box((1.16,1.64,.045),(0,0,0),EDGE,.006);b.plane((1.09,1.55),(0,0,.026),SLOGAN);register(b,'dressing')
b=Build('GlassDecal');b.plane((1.45,.267),(0,0,0),GLASSLOGO);register(b,'dressing')
b=Build('FloorLabel');b.plane((1.43,.22),(0,.004,0),FLOORLABEL,(-math.pi/2,0,0));register(b,'dressing')
b=Build('SessionFigure');SKIN=mat('SkinNeutral','aa917b',0,.85);COAT=surface('FigureCoat','666d64','rug',.8,0,256);HAIR=mat('Hair','272624',0,.94)
for x in [-.105,.105]:b.box((.14,.63,.16),(x,.385,0),EDGE,.003);b.box((.16,.105,.26),(x,.052,.033),RUBBER,.004)
b.box((.39,.53,.23),(0,.958,0),COAT,.007);b.box((.05,.49,.012),(0,.96,.124),CHROME,.002)
for x in [-.255,.255]:b.box((.12,.45,.17),(x,.97,0),COAT,.006);b.box((.092,.13,.11),(x,.70,.015),SKIN,.004)
b.box((.22,.25,.22),(0,1.375,0),SKIN,.003);b.box((.231,.07,.23),(0,1.499,-.007),HAIR,.002);register(b,'dressing')

# Data-driven assemblies, with instance identities retained. No live agents.
LAYOUTS={}
def layout(room):arr=[];LAYOUTS[room]=arr;return arr
def place(arr,asset,x=0,y=0,z=0,ry=0,scale=1,id=None):arr.append(dict(id=id or f'{asset}-{len(arr):03}',asset=asset,position=[x,y,z],rotation=[0,ry,0],scale=scale))
def shell(arr,w=10.8,d=8.4,glass=True):
 for i in range(round(w/1.2)):
  for j in range(round(d/1.2)+1):
   place(arr,'FloorTile',-w/2+.6+i*1.2,0,-d/2+.6+j*1.2,((i*3+j)%4)*math.pi/2)
   place(arr,'FloorPlinth',-w/2+.6+i*1.2,0,-d/2+.6+j*1.2)
 for i in range(round(w/1.2)):
  x=-w/2+.6+i*1.2;place(arr,'WallPanel',x,0,-d/2);place(arr,'PipeRun',x,2.93,-d/2+.22)
 for j in range(round(d/1.2)):
  z=-d/2+.6+j*1.2;place(arr,'WallPanel',-w/2,0,z,math.pi/2);place(arr,'PipeRun',-w/2+.22,2.93,z,math.pi/2)
 for x,z in [(-w/2,-d/2),(w/2,-d/2),(-w/2,d/2),(w/2,d/2)]:place(arr,'StructuralColumn',x,0,z)
 for x in np.arange(-w/2+1.2,w/2,2.4):place(arr,'CeilingBeam',float(x),3.13,-d/2);place(arr,'LinearLight',float(x),2.89,-d/2+.24)
 for z in np.arange(-d/2+1.2,d/2,2.4):place(arr,'CeilingBeam',-w/2,3.13,float(z),math.pi/2);place(arr,'LinearLight',-w/2+.24,2.89,float(z),math.pi/2)
 if glass:
  place(arr,'GlassBay',-w/2+.6,0,d/2);place(arr,'DoubleGlassDoor',-w/2+2.4,0,d/2);place(arr,'EntrancePortal',-w/2+2.4,0,d/2)
  count=round((w-3.6)/1.2);i=0
  while i<count:
   if count-i>=2:place(arr,'WideGlassBay',-w/2+3.6+1.2+i*1.2,0,d/2);i+=2
   else:place(arr,'GlassBay',w/2-.6,0,d/2);i+=1
  count=round(d/1.2);j=0
  while j<count:
   if count-j>=2:place(arr,'WideGlassBay',w/2,0,-d/2+1.2+j*1.2,math.pi/2);j+=2
   else:place(arr,'GlassBay',w/2,0,d/2-.6,math.pi/2);j+=1
  for xx in np.arange(-w/2+1.2,w/2,2.4):place(arr,'FacadeHeader',float(xx),3.2,d/2)
  for zz in np.arange(-d/2+1.2,d/2,2.4):place(arr,'FacadeHeader',w/2,3.2,float(zz),math.pi/2)
  place(arr,'GlassDecal',1.55,1.93,d/2+.071)
def desk(arr,x,z,ry=0,twin=True):
 place(arr,'Workbench',x,0,z,ry)
 def at(xx,y,zz,asset,angle=0):place(arr,asset,x+xx*math.cos(ry)+zz*math.sin(ry),y,z-xx*math.sin(ry)+zz*math.cos(ry),ry+angle)
 for dx in ([-.63,.63] if twin else [0]):
  at(dx,.797,-.16,'Monitor');at(dx,.799,.225,'Keyboard');at(dx+.30,.80,.25,'Mouse');at(dx,0,.91,'OfficeChair',math.pi);at(dx-.32,.8,.27,'Mug')
arr=layout('Research');shell(arr)
place(arr,'MonitorWall',2.0,0,-3.92);desk(arr,1.65,-3.25);desk(arr,1.0,.30);desk(arr,1.0,-.68,math.pi)
place(arr,'DGLogoPanel',-1.70,1.7,-3.985);place(arr,'ServerRack',-4.54,0,-3.47);place(arr,'Bookcase',-3.54,0,-3.73)
place(arr,'Sofa',-4.83,0,-.52,math.pi/2);place(arr,'CoffeeTable',-3.72,0,-.52,math.pi/2);place(arr,'BookStack',-3.72,.412,-.35)
place(arr,'SloganPanel',-5.27,1.98,-.7,math.pi/2);place(arr,'SideCabinet',-2.7,0,-3.72);place(arr,'CoffeeMachine',-2.96,.87,-3.70)
for x,z in [(-4.83,1.20),(-4.78,-2.72),(4.8,-3.47),(4.87,3.58)]:place(arr,'Planter',x,0,z)
place(arr,'ServerRack',4.95,0,-2.08,-math.pi/2);place(arr,'Rug',1.0,.008,-.10,0,1.18);place(arr,'UtilityCart',4.77,0,2.23,-math.pi/2);place(arr,'BookStack',4.80,.7,2.23)
place(arr,'FloorLabel',-3.6,.01,4.70);place(arr,'SessionFigure',-3.4,0,3.40,0);place(arr,'SessionFigure',1.65,0,-2.48,math.pi);place(arr,'SessionFigure',1.7,0,1.37,math.pi)
arr=layout('Lobby');shell(arr,9.6,8.4)
place(arr,'ReceptionDesk',-.55,0,-.8);place(arr,'Monitor',-.90,.78,-1.39,math.pi);place(arr,'Monitor',.30,.78,-1.39,math.pi);place(arr,'SessionFigure',-.4,0,-1.68);place(arr,'BookStack',-1.67,1.14,-.7);place(arr,'DeskPlant',.89,1.13,-.75)
place(arr,'DGLogoPanel',-.3,1.79,-3.985);place(arr,'DGLogoPanel',-4.67,1.90,-.96,math.pi/2);place(arr,'Sofa',-4.20,0,-.1,math.pi/2);place(arr,'CoffeeTable',-3.22,0,-.1,math.pi/2);place(arr,'BookStack',-3.22,.41,.04);place(arr,'Rug',-.5,0,-.55,0,1.08)
for x,z in [(-4.12,-3.62),(-4.19,1.59),(1.25,-3.59),(4.15,3.62),(4.12,-3.48)]:place(arr,'Planter',x,0,z)
place(arr,'AccessGate',2.35,0,.35);place(arr,'AccessGate',3.34,0,.35);place(arr,'Kiosk',4.29,0,-1.05,-.23);place(arr,'FloorLabel',-3.0,0,4.7);place(arr,'SessionFigure',2.65,0,1.55,math.pi);place(arr,'SloganPanel',-2.65,1.86,-3.985);place(arr,'WallDisplay',3.02,2.09,-4.02);place(arr,'ServerRack',3.94,0,-3.43)
arr=layout('Meeting');shell(arr)
place(arr,'ConferenceTable',.40,0,-.28);place(arr,'Rug',.4,0,-.28,0,1.62)
for x in [-1.15,.4,1.95]:
 for z,ry in [(1.00,math.pi),(-1.57,0)]:place(arr,'OfficeChair',x,0,z,ry)
 for z,ry in [(.12,math.pi),(-.70,0)]:place(arr,'Tablet',x,.86,z,ry)
place(arr,'DeskPlant',0,.849,-.28);place(arr,'Mug',-1.61,.843,.21);place(arr,'BookStack',2.14,.85,-.3)
place(arr,'MonitorWall',2.05,0,-3.94);place(arr,'DGLogoPanel',-2.39,1.78,-3.98);place(arr,'SideCabinet',-4.72,0,-.75,math.pi/2);place(arr,'CoffeeMachine',-4.72,.87,-1.07,math.pi/2);place(arr,'SloganPanel',-5.27,2.0,-.98,math.pi/2);place(arr,'Bookcase',-4.63,0,-3.69)
for x,z in [(-4.72,1.18),(-3.52,-3.60),(4.84,-3.58),(4.90,3.60)]:place(arr,'Planter',x,0,z)
place(arr,'SessionFigure',.10,0,-2.60);place(arr,'SessionFigure',2.8,0,.80,math.pi)
arr=layout('Corridor');shell(arr,10.8,6.0)
place(arr,'DGLogoPanel',-3.90,1.76,-2.78);place(arr,'ServerRack',-2.35,0,-2.50);place(arr,'WallDisplay',-.69,2.08,-2.82);place(arr,'Kiosk',-.66,0,-2.40);place(arr,'SloganPanel',1.17,1.8,-2.80);place(arr,'ServerRack',2.40,0,-2.46);place(arr,'DGLogoPanel',4.04,1.75,-2.8)
for x in [-3.6,0,3.6]:place(arr,'GlassDoor',x,0,1.2)
for x in [-4.8,-2.4,-1.2,1.2,2.4,4.8]:place(arr,'GlassBay',x,0,1.2)
place(arr,'Sofa',-2.85,0,.08);place(arr,'SessionFigure',.15,0,.04,math.pi/2)
for x,z in [(-4.83,-1.94),(4.8,-2.07),(-.1,.6)]:place(arr,'Planter',x,0,z)
place(arr,'FloorLabel',.6,0,.70);place(arr,'GlassDecal',2.5,1.65,1.27)

CATALOG=[];SCENES={}
for name,(b,cat) in ASSETS.items():
 s=b.scene();SCENES[name]=s;raw=s.export(file_type='glb');(OUT/f'{name}.glb').write_bytes(raw);bounds=s.bounds
 CATALOG.append(dict(id=name,category=cat,url=f'models/{name}.glb',dimensions=np.round(bounds[1]-bounds[0],4).tolist(),bounds=np.round(bounds,5).tolist(),triangles=sum(len(m.faces) for m in s.geometry.values()),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 print(name,len(raw),flush=True)
for room,items in LAYOUTS.items():
 s=tm.Scene()
 for asset in sorted({item['asset'] for item in items}):
  for gn,gm in SCENES[asset].geometry.items():s.geometry[f'{asset}_{gn}']=gm
 for item in items:
  root=item['id'];t=tm.transformations.rotation_matrix(item['rotation'][1],[0,1,0]);t[:3,:3]*=item['scale'];t[:3,3]=item['position'];s.graph.update(frame_to=root,matrix=t)
  for gn in SCENES[item['asset']].geometry:s.graph.update(frame_from=root,frame_to=f'{root}_{gn}',matrix=np.eye(4),geometry=f'{item["asset"]}_{gn}')
 raw=s.export(file_type='glb');(OUT/f'{room}Room.glb').write_bytes(raw);(ROOT/'public'/f'{room.lower()}.layout.json').write_text(json.dumps(items,indent=2));print('ROOM',room,len(raw),flush=True)
(ROOT/'public/catalog.json').write_text(json.dumps(CATALOG,indent=2));(ROOT/'public/layouts.json').write_text(json.dumps(LAYOUTS,indent=2))
print('COMPLETE:',len(CATALOG),'assets;',len(LAYOUTS),'rooms')
