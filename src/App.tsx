import './north-star.css'
import {Suspense,useEffect,useMemo,useRef,useState,Component,type ReactNode,type Dispatch,type SetStateAction} from 'react'
import {Canvas,useThree,useFrame} from '@react-three/fiber'
import {Bounds,OrbitControls,Html,useProgress,ContactShadows} from '@react-three/drei'
import {ACESFilmicToneMapping,OrthographicCamera,Mesh,Box3,Box3Helper,Vector3,Euler,Matrix4,Quaternion,type Material} from 'three'
import {ContactGrounding} from './kit/core/ContactGrounding'
import {ViewportQuality} from './kit/core/ViewportQuality'
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
 const orbit=useRef<OrbitControlsImpl>(null);const {camera,size,invalidate}=useThree();const parts=view.endsWith('-parts')
 useEffect(()=>{
  const c=camera as OrthographicCamera
  c.position.set(13,20,16.5);c.zoom=Math.min(size.width/14.1,(size.height-120)/14.2)
  c.lookAt(0,1.2,.35);c.updateProjectionMatrix();orbit.current?.target.set(0,1.2,.35);orbit.current?.update();invalidate()
 },[camera,size.width,size.height,view,reset,invalidate])
 return <OrbitControls ref={orbit} makeDefault enableDamping enablePan={parts} minZoom={parts?1:12} maxZoom={parts?2000:150} minPolarAngle={parts?.05:Math.PI*.13} maxPolarAngle={parts?Math.PI*.49:Math.PI*.37} minAzimuthAngle={parts?-Infinity:.12} maxAzimuthAngle={parts?Infinity:Math.PI*.45}/>
}
function Selection({item}:{item:LayoutItem|null}){
 const {scene,invalidate}=useThree()
 useEffect(()=>{
  if(!item)return;const asset=catalog.find(a=>a.id===item.asset);if(!asset)return
  const box=new Box3(new Vector3(...asset.bounds[0]),new Vector3(...asset.bounds[1]))
  const matrix=new Matrix4().compose(new Vector3(...item.position),new Quaternion().setFromEuler(new Euler(...item.rotation)),new Vector3().setScalar(item.scale));box.applyMatrix4(matrix)
  const h=new Box3Helper(box,0x53d6ad);scene.add(h);invalidate()
  return()=>{scene.remove(h);h.geometry.dispose();(h.material as Material).dispose();invalidate()}
 },[item,scene,invalidate]);return null
}
function Diagnostics({enabled}:{enabled:boolean}){
 const {scene,gl,camera,invalidate,controls}=useThree(),state=useRef({last:0,updated:0,samples:[] as number[],dragging:false})
 useEffect(()=>{
  if(!enabled)return
  const old=gl.info.autoReset;gl.info.autoReset=false
  const ctrl=controls as OrbitControlsImpl|null,start=()=>{state.current.dragging=true;state.current.samples=[];state.current.last=0},end=()=>{state.current.dragging=false}
  ctrl?.addEventListener('start',start);ctrl?.addEventListener('end',end)
  // Exposed only with the optional monitor, for reproducible browser checks.
  Object.assign(window,{__scene:scene,__gl:gl,__camera:camera,__invalidate:invalidate})
  const timer=setInterval(()=>{if(performance.now()-state.current.last>500){const el=document.getElementById('perf-hud');if(el)el.dataset.idle='true'}},500)
  return()=>{clearInterval(timer);gl.info.autoReset=old;ctrl?.removeEventListener('start',start);ctrl?.removeEventListener('end',end)}
 },[enabled,scene,gl,camera,invalidate,controls])
 useFrame(()=>{
  if(!enabled)return
  gl.info.reset();const now=performance.now(),s=state.current,dt=now-s.last
  // First frame after on-demand idle is not a slow rendered frame.
  if(s.last&&(dt<250||s.dragging))s.samples.push(dt);else s.samples=[]
  s.last=now;if(now-s.updated<600)return;s.updated=now
  const sample=s.samples.splice(0);const mean=sample.length?sample.reduce((a,b)=>a+b,0)/sample.length:0
  sample.sort((a,b)=>a-b);const p95=sample[Math.min(sample.length-1,Math.floor(sample.length*.95))]??0
  queueMicrotask(()=>{
   let meshes=0;scene.traverse(n=>{if(n instanceof Mesh)meshes++});const r=gl.info.render,mem=gl.info.memory
   const data={fps:mean?Math.round(1000/mean):null,frameMs:mean,p95Ms:p95,calls:r.calls,triangles:r.triangles,meshes,textures:mem.textures,dpr:gl.getPixelRatio()}
   Object.assign(window,{__DG_METRICS__:data});const hud=document.getElementById('perf-hud')
   if(hud){hud.dataset.idle='false';hud.textContent=`${data.fps??'—'} FPS · ${mean.toFixed(1)} ms · p95 ${p95.toFixed(1)} ms\n${r.calls} draws · ${r.triangles.toLocaleString()} tris\n${meshes} meshes · ${mem.textures} textures · DPR ${data.dpr.toFixed(2)}`}
  })
 },-100)
 return null
}
function Exposure({value}:{value:number}){const {gl,invalidate}=useThree();useEffect(()=>{gl.toneMappingExposure=value;invalidate()},[value,gl,invalidate]);return null}
export function App(){
 const params=new URLSearchParams(location.search)
 const [room,setRoom]=useState(params.get('room')&&layouts[params.get('room')!]?params.get('room')!:'Research'),[mode,setMode]=useState<'rooms'|'parts'>(params.has('asset')?'parts':'rooms'),[asset,setAsset]=useState(catalog.some(a=>a.id===params.get('asset'))?params.get('asset')!:'ReceptionDesk')
 const [mobile,setMobile]=useState(()=>matchMedia('(max-width:760px)').matches)
 const [wire,setWire]=useState(false),[glass,setGlass]=useState(true),[figures,setFigures]=useState(true),[facade,setFacade]=useState(true),[fx,setFx]=useState(params.get('fx')==='on'),[reflect,setReflect]=useState(params.get('reflections')==='on'),[exposure,setExposure]=useState(1.1)
 const [quality,setQuality]=useState<'balanced'|'high'>('balanced'),[showPerf,setShowPerf]=useState(params.get('perf')==='1')
 const [lighting,setLighting]=useState<'cinematic'|'inspection'>('cinematic'),[reset,setReset]=useState(0),[query,setQuery]=useState(''),[selected,setSelected]=useState<LayoutItem|null>(null),[drawer,setDrawer]=useState(false)
 useEffect(()=>{const mq=matchMedia('(max-width:760px)');const f=()=>setMobile(mq.matches);mq.addEventListener('change',f);return()=>mq.removeEventListener('change',f)},[])
 const shown=useMemo(()=>catalog.filter(a=>`${a.id} ${a.category}`.toLowerCase().includes(query.toLowerCase())),[query])
 const info=catalog.find(a=>a.id===(mode==='parts'?asset:selected?.asset)),settings=useMemo(()=>({basePath:'./models',wireframe:wire,glass,emission:2,shadowMode:'lite' as const}),[wire,glass])
 const download=()=>{const name=mode==='parts'?asset:selected?.asset??`${room}Room`;const a=document.createElement('a');a.href=window.__DG_ASSETS__?.[`models/${name}.glb`]??`./models/${name}.glb`;a.download=`${name}.glb`;a.click()}
 const toggles:[string,boolean,Dispatch<SetStateAction<boolean>>][]=[['Glass',glass,setGlass],['Frontage',facade,setFacade],['Wireframe',wire,setWire],['Scale figures',figures,setFigures],['Bloom / AO',fx,setFx],['Floor reflections',reflect,setReflect],['Performance monitor',showPerf,setShowPerf]]
 return <div className="app">
  <header><div className="brand"><b>dg<span>_</span></b><div>Digital Gnosis<span>.</span><small>SPATIAL COMPONENT LIBRARY / 01</small></div></div><div className="header-right"><span className="status-dot"/>{catalog.length} ASSETS<button className="mobile-menu" aria-label="Show controls" onClick={()=>setDrawer(!drawer)}>☰</button></div></header>
  <nav aria-label="Preview mode"><button className={mode==='rooms'?'active':''} onClick={()=>{setMode('rooms');setSelected(null)}}>Room studies</button><button className={mode==='parts'?'active':''} onClick={()=>{setMode('parts');setSelected(null);setDrawer(true)}}>Components</button><span className="nav-note">Real geometry. Reusable pieces.</span></nav>
  <main><aside className={drawer?'open':''}><div className="eyebrow">{mode==='rooms'?'ASSEMBLED FROM THE KIT':'COMPONENT CATALOG'}</div>
   {mode==='rooms'?<div className="room-list">{Object.keys(layouts).map((name,i)=><button key={name} className={name===room?'active':''} onClick={()=>{setRoom(name);setSelected(null);setDrawer(false)}}><span>0{i+1}</span><div>{name}<small>{layouts[name].length} placed instances</small></div><span>↗</span></button>)}</div>:<><input aria-label="Search components" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Find a piece…"/><div className="asset-list">{shown.map(a=><button key={a.id} className={asset===a.id?'active':''} onClick={()=>{setAsset(a.id);setDrawer(false)}}><span>{a.id}</span><small>{a.category}</small></button>)}</div></>}
   <div className="controls"><div className="eyebrow">IMAGE QUALITY</div><div className="segmented"><button className={quality==='balanced'?'active':''} onClick={()=>setQuality('balanced')}>Balanced</button><button className={quality==='high'?'active':''} onClick={()=>setQuality('high')}>High</button></div><div className="eyebrow">APPEARANCE</div><div className="segmented"><button className={lighting==='cinematic'?'active':''} onClick={()=>setLighting('cinematic')}>Cinematic</button><button className={lighting==='inspection'?'active':''} onClick={()=>setLighting('inspection')}>Inspection</button></div><label className="range">Exposure <output>{exposure.toFixed(2)}</output><input aria-label="Exposure" type="range" min=".6" max="2.6" step=".05" value={exposure} onChange={e=>setExposure(+e.target.value)}/></label>
   {toggles.map(([label,value,setter])=><label className="toggle" key={label}><span>{label}</span><input type="checkbox" checked={value} onChange={e=>setter(e.target.checked)}/></label>)}<p className="subtle">Anti-aliasing stays on. Sharpness restores when the camera stops; optional reflections add GPU cost.</p></div>
   <div className="inspector"><div className="eyebrow">{info?'SELECTED COMPONENT':'DESIGN PREVIEW'}</div><h3>{info?.id??room}</h3>{info?<><p>{info.dimensions.map(v=>v.toFixed(2)).join(' × ')} m</p><p>{info.triangles.toLocaleString()} triangles · {(info.bytes/1024).toFixed(0)} KB</p><code>{`<${info.id} />`}</code></>:<p>Tap a piece to inspect it. Screens and figures are demonstration content, not live work.</p>}<button className="download" onClick={download}>↓ Export {info?'selected piece':'room'} GLB</button></div>
  </aside><section className="stage" aria-label="Interactive 3D preview"><Boundary><Canvas frameloop="demand" orthographic camera={{position:[13,14.2,16.5],zoom:48,near:.1,far:120}} dpr={1.75} shadows gl={{antialias:true,alpha:false,powerPreference:'high-performance',toneMapping:ACESFilmicToneMapping,toneMappingExposure:exposure}}>
   <color attach="background" args={['#091115']}/><Exposure value={exposure}/><CameraRig view={`${room}-${mode}`} reset={reset}/><ViewportQuality mobile={mobile} quality={quality}/><Diagnostics enabled={showPerf}/>
   <AssetContext.Provider value={settings}><Suspense fallback={<Loading/>}><DGLightingRig mobile={mobile} mode={lighting} revision={`${room}-${mode}-${asset}-${figures}-${facade}-${glass}`}/>
    {mode==='rooms'?<group key={room}><RoomLayout items={layouts[room]} onSelect={setSelected} showFigures={figures} hideFacade={!facade}/>{!wire?<ContactGrounding items={layouts[room]} showFigures={figures}/>:null}{reflect?<ReflectiveFloor width={room==='Lobby'?9.6:10.8} depth={room==='Corridor'?7.2:9.6} resolution={mobile?256:512}/>:null}<Selection item={selected}/></group>:<Bounds key={asset} fit clip observe margin={1.7}><DGAsset asset={asset}/></Bounds>}
    {mode==='parts'?<ContactShadows key={asset} position={[0,-.34,0]} opacity={.4} scale={18} blur={2.7} far={7} frames={1} resolution={512}/>:null}
   </Suspense></AssetContext.Provider>{fx?<SceneEffects ao={!mobile}/>:null}
  </Canvas></Boundary>{showPerf?<div id="perf-hud" className="perf-hud">Move camera to measure</div>:null}<div className="stage-caption"><span>{mode==='rooms'?room.toUpperCase():asset}</span><small>{mode==='rooms'?'48 independent models / authored room layout':'Exported asset / Y-up / meters'}</small></div><div className="stage-tools"><button onClick={()=>setReset(v=>v+1)}>↗ Reset view</button><button onClick={download}>↓ GLB</button></div><div className="gestures">Drag to orbit · Pinch to zoom · Reset restores the reference angle</div></section></main>
  <footer><span><i/>Design preview · no agents connected</span><span>R3F / THREE.JS · MODULAR KIT</span></footer>
 </div>
}
