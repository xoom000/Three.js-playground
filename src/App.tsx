import {Suspense,useEffect,useMemo,useRef,useState,Component,type ReactNode,type Dispatch,type SetStateAction} from 'react'
import {Canvas,useThree,useFrame} from '@react-three/fiber'
import {Bounds,OrbitControls,Html,useProgress,ContactShadows} from '@react-three/drei'
import {ACESFilmicToneMapping,BoxHelper,OrthographicCamera,Mesh,type Material} from 'three'
import type {OrbitControls as OrbitControlsImpl} from 'three-stdlib'
import {DGAsset} from './kit/core/DGAsset'
import {AssetContext} from './kit/core/AssetContext'
import {DGLightingRig} from './kit/core/DGLightingRig'
import {SceneEffects} from './kit/core/SceneEffects'
import {ReflectiveFloor} from './kit/core/ReflectiveFloor'
import {RoomLayout,type LayoutItem} from './kit/scenes/RoomLayout'
import {catalog} from './catalog'
import {layouts} from './layouts'
class Boundary extends Component<{children:ReactNode},{error:string|null}>{
 state={error:null as string|null};static getDerivedStateFromError(e:Error){return{error:e.message}}
 render(){return this.state.error?<div className="failure"><h2>Preview could not load.</h2><p>{this.state.error}</p><p>Model files must remain alongside this app. Try reloading.</p><button onClick={()=>location.reload()}>Reload</button></div>:this.props.children}
}
function Loading(){const {progress}=useProgress();return <Html center><div className="loading">Loading actual models<br/><b>{progress.toFixed(0)}%</b></div></Html>}
function CameraRig({view,reset}:{view:string;reset:number}){
 const orbit=useRef<OrbitControlsImpl>(null);const {camera,size,invalidate}=useThree()
 useEffect(()=>{
  const c=camera as OrthographicCamera;c.position.set(13,14.2,16.5);c.zoom=Math.min(size.width/15.7,size.height/13.4);c.lookAt(0,1.3,.5);c.updateProjectionMatrix();orbit.current?.target.set(0,1.3,.5);orbit.current?.update();invalidate()
 },[camera,size,view,reset,invalidate])
 return <OrbitControls ref={orbit} makeDefault enableDamping minZoom={10} maxZoom={500} maxPolarAngle={Math.PI*.49}/>
}
function Selection({id}:{id:string|null}){
 const {scene,invalidate}=useThree()
 useEffect(()=>{if(!id)return;const node=scene.getObjectByName(id);if(!node)return;const h=new BoxHelper(node,0x53d6ad);scene.add(h);invalidate();return()=>{scene.remove(h);h.geometry.dispose();(h.material as Material).dispose();invalidate()}},[id,scene,invalidate]);return null
}
function Diagnostics({enabled}:{enabled:boolean}){
 const {scene,gl}=useThree(),sample=useRef({frames:0,seconds:0})
 useFrame((_,delta)=>{
  if(!enabled)return
  const s=sample.current;s.frames++;s.seconds+=Math.min(delta,.25)
  if(s.seconds<.6)return
  let meshes=0;scene.traverse(n=>{if(n instanceof Mesh)meshes++})
  const fps=Math.round(s.frames/s.seconds),ms=s.seconds/s.frames*1000,render=gl.info.render,memory=gl.info.memory,hud=document.getElementById('perf-hud')
  if(hud){hud.dataset.level=fps<30?'bad':fps<50?'warn':'good';hud.innerHTML=`<b>${fps} FPS</b> · ${ms.toFixed(1)} ms<br>${render.calls} draws · ${render.triangles.toLocaleString()} tris<br>${meshes} meshes · ${memory.geometries} geos · ${memory.textures} tex<br>DPR ${gl.getPixelRatio().toFixed(2)}`}
  s.frames=0;s.seconds=0
 })
 return null
}
function Exposure({value}:{value:number}){const {gl,invalidate}=useThree();useEffect(()=>{gl.toneMappingExposure=value;invalidate()},[value,gl,invalidate]);return null}
export function App(){
 const params=new URLSearchParams(location.search)
 const [room,setRoom]=useState(params.get('room')&&layouts[params.get('room')!]?params.get('room')!:'Research'),[mode,setMode]=useState<'rooms'|'parts'>(params.has('asset')?'parts':'rooms'),[asset,setAsset]=useState(catalog.some(a=>a.id===params.get('asset'))?params.get('asset')!:'ReceptionDesk')
 const [mobile,setMobile]=useState(()=>matchMedia('(max-width:760px)').matches)
 const [wire,setWire]=useState(false),[glass,setGlass]=useState(true),[figures,setFigures]=useState(true),[facade,setFacade]=useState(true),[fx,setFx]=useState(params.get('fx')==='on'),[reflect,setReflect]=useState(params.get('reflections')==='on'),[exposure,setExposure]=useState(1.3)
 const [lighting,setLighting]=useState<'cinematic'|'inspection'>('cinematic'),[reset,setReset]=useState(0),[query,setQuery]=useState(''),[selected,setSelected]=useState<LayoutItem|null>(null),[drawer,setDrawer]=useState(false)
 useEffect(()=>{const mq=matchMedia('(max-width:760px)');const f=()=>setMobile(mq.matches);mq.addEventListener('change',f);return()=>mq.removeEventListener('change',f)},[])
 const shown=useMemo(()=>catalog.filter(a=>`${a.id} ${a.category}`.toLowerCase().includes(query.toLowerCase())),[query])
 const info=catalog.find(a=>a.id===(mode==='parts'?asset:selected?.asset)),shadowMode=mobile?'lite' as const:'full' as const,settings=useMemo(()=>({basePath:'./models',wireframe:wire,glass,emission:2.8,shadowMode}),[wire,glass,shadowMode]),showPerf=mobile||params.get('perf')==='1'
 const download=()=>{const name=mode==='parts'?asset:selected?.asset??`${room}Room`;const a=document.createElement('a');a.href=window.__DG_ASSETS__?.[`models/${name}.glb`]??`./models/${name}.glb`;a.download=`${name}.glb`;a.click()}
 const toggles:[string,boolean,Dispatch<SetStateAction<boolean>>][]=[['Glass',glass,setGlass],['Frontage',facade,setFacade],['Wireframe',wire,setWire],['Scale figures',figures,setFigures],['Bloom / AO',fx,setFx],['Floor reflections',reflect,setReflect]]
 return <div className="app">
  <header><div className="brand"><b>dg<span>_</span></b><div>Digital Gnosis<span>.</span><small>SPATIAL COMPONENT LIBRARY / 01</small></div></div><div className="header-right"><span className="status-dot"/>{catalog.length} ASSETS<button className="mobile-menu" aria-label="Show controls" onClick={()=>setDrawer(!drawer)}>☰</button></div></header>
  <nav aria-label="Preview mode"><button className={mode==='rooms'?'active':''} onClick={()=>{setMode('rooms');setSelected(null)}}>Room studies</button><button className={mode==='parts'?'active':''} onClick={()=>{setMode('parts');setSelected(null);setDrawer(true)}}>Components</button><span className="nav-note">Real geometry. Reusable pieces.</span></nav>
  <main><aside className={drawer?'open':''}><div className="eyebrow">{mode==='rooms'?'ASSEMBLED FROM THE KIT':'COMPONENT CATALOG'}</div>
   {mode==='rooms'?<div className="room-list">{Object.keys(layouts).map((name,i)=><button key={name} className={name===room?'active':''} onClick={()=>{setRoom(name);setSelected(null);setDrawer(false)}}><span>0{i+1}</span><div>{name}<small>{layouts[name].length} placed instances</small></div><span>↗</span></button>)}</div>:<><input aria-label="Search components" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Find a piece…"/><div className="asset-list">{shown.map(a=><button key={a.id} className={asset===a.id?'active':''} onClick={()=>{setAsset(a.id);setDrawer(false)}}><span>{a.id}</span><small>{a.category}</small></button>)}</div></>}
   <div className="controls"><div className="eyebrow">APPEARANCE</div><div className="segmented"><button className={lighting==='cinematic'?'active':''} onClick={()=>setLighting('cinematic')}>Cinematic</button><button className={lighting==='inspection'?'active':''} onClick={()=>setLighting('inspection')}>Inspection</button></div><label className="range">Exposure <output>{exposure.toFixed(2)}</output><input aria-label="Exposure" type="range" min=".6" max="2.6" step=".05" value={exposure} onChange={e=>setExposure(+e.target.value)}/></label>
   {toggles.map(([label,value,setter])=><label className="toggle" key={label}><span>{label}</span><input type="checkbox" checked={value} onChange={e=>setter(e.target.checked)}/></label>)}<p className="subtle">Optional effects add GPU cost. Start with them off on a phone.</p></div>
   <div className="inspector"><div className="eyebrow">{info?'SELECTED COMPONENT':'DESIGN PREVIEW'}</div><h3>{info?.id??room}</h3>{info?<><p>{info.dimensions.map(v=>v.toFixed(2)).join(' × ')} m</p><p>{info.triangles.toLocaleString()} triangles · {(info.bytes/1024).toFixed(0)} KB</p><code>{`<${info.id} />`}</code></>:<p>Tap a piece to inspect it. Screens and figures are demonstration content, not live work.</p>}<button className="download" onClick={download}>↓ Export {info?'selected piece':'room'} GLB</button></div>
  </aside><section className="stage" aria-label="Interactive 3D preview"><Boundary><Canvas frameloop="demand" orthographic camera={{position:[13,14.2,16.5],zoom:48,near:.1,far:120}} dpr={mobile?1:1.25} shadows gl={{antialias:!mobile,alpha:false,powerPreference:'high-performance',toneMapping:ACESFilmicToneMapping,toneMappingExposure:exposure}}>
   <color attach="background" args={['#091115']}/><Exposure value={exposure}/><CameraRig view={`${room}-${mode}`} reset={reset}/><Diagnostics enabled={showPerf}/>
   <AssetContext.Provider value={settings}><Suspense fallback={<Loading/>}><DGLightingRig key={`lights-${room}-${mode}-${figures}-${facade}`} mobile={mobile} mode={lighting}/>
    {mode==='rooms'?<group key={room}><RoomLayout items={layouts[room]} onSelect={setSelected} showFigures={figures} hideFacade={!facade}/>{reflect?<ReflectiveFloor width={room==='Lobby'?9.6:10.8} depth={room==='Corridor'?7.2:9.6} resolution={mobile?256:512}/>:null}<Selection id={selected?.id??null}/></group>:<Bounds key={asset} fit clip observe margin={1.7}><DGAsset asset={asset}/></Bounds>}
    {mode==='parts'?<ContactShadows position={[0,-.34,0]} opacity={.4} scale={18} blur={2.7} far={7} frames={1} resolution={mobile?256:512}/>:null}
   </Suspense></AssetContext.Provider>{fx?<SceneEffects ao={!mobile}/>:null}
  </Canvas></Boundary>{showPerf?<div id="perf-hud" style={{position:'fixed',right:10,top:112,zIndex:20,pointerEvents:'none',padding:'8px 10px',borderRadius:10,border:'1px solid #29423d',background:'rgba(4,10,12,.82)',color:'#b8c9c5',font:'11px ui-monospace, SFMono-Regular, Menlo, monospace',lineHeight:1.45,backdropFilter:'blur(8px)'}}>PERF · move camera to sample</div>:null}<div className="stage-caption"><span>{mode==='rooms'?room.toUpperCase():asset}</span><small>{mode==='rooms'?'48 independent models / authored room layout':'Exported asset / Y-up / meters'}</small></div><div className="stage-tools"><button onClick={()=>setReset(v=>v+1)}>↗ Reset view</button><button onClick={download}>↓ GLB</button></div><div className="gestures">Drag to orbit · Pinch to zoom · Two fingers to pan</div></section></main>
  <footer><span><i/>Design preview · no agents connected</span><span>R3F / THREE.JS · MODULAR KIT</span></footer>
 </div>
}
