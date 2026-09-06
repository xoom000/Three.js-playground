import {useEffect} from 'react'
import {useThree} from '@react-three/fiber'
import {Environment,Lightformer} from '@react-three/drei'
export interface LightingProps{mobile?:boolean;mode?:'cinematic'|'inspection';revision?:string}
function StaticShadows({revision}:{revision:string}){
 const {gl,invalidate}=useThree()
 useEffect(()=>{
  const was=gl.shadowMap.autoUpdate;gl.shadowMap.autoUpdate=false
  const refresh=()=>{gl.shadowMap.needsUpdate=true;invalidate()}
  refresh();const timer=setTimeout(refresh,120)
  return()=>{clearTimeout(timer);gl.shadowMap.autoUpdate=was}
 },[revision,gl,invalidate]);return null
}
/** One cached key shadow, restrained fill, and an environment captured once.
 * Cached shadow maps are not baked GI/lightmaps. Rebuild on room/visibility changes.
 */
export function DGLightingRig({mobile=false,mode='cinematic',revision=''}:LightingProps){
 const inspection=mode==='inspection'
 return <>
  <StaticShadows revision={`${revision}:${mode}:${mobile}`}/>
  <hemisphereLight args={['#b5cfce','#101c1a',inspection?.9:.36]}/>
  <directionalLight position={[-3.6,9,4]} color="#ffe1b8" intensity={inspection?2.7:2.3} castShadow shadow-mapSize={[mobile?1024:2048,mobile?1024:2048]} shadow-camera-left={-8} shadow-camera-right={8} shadow-camera-top={8} shadow-camera-bottom={-8} shadow-camera-near={.5} shadow-camera-far={30} shadow-bias={-.00045} shadow-normalBias={.035}/>
  <directionalLight position={[4,6,1]} color="#b0c9d4" intensity={inspection?1.2:.75}/>
  <pointLight position={[1.5,2.4,-3.3]} color="#42cddd" intensity={inspection?4:10} distance={8} decay={2}/>
  <pointLight position={[3.6,2.2,-3.25]} color="#ce3199" intensity={inspection?3:9} distance={7} decay={2}/>
  <pointLight position={[-3,2.5,2.9]} color="#ffcb8b" intensity={8} distance={6} decay={2}/>
  <Environment resolution={mobile?64:128} frames={1} environmentIntensity={inspection?.7:.54}>
   <Lightformer intensity={2.8} position={[0,5,0]} rotation={[Math.PI/2,0,0]} scale={[11,8,1]} color="#ddd5c6"/>
   <Lightformer intensity={1.6} position={[7,2,4]} rotation={[0,-Math.PI/2,0]} scale={[10,3,1]} color="#9bbbc8"/>
   <Lightformer intensity={1.4} position={[-5,3,2]} rotation={[0,Math.PI/2,0]} scale={[6,3,1]} color="#e4b98e"/>
  </Environment>
 </>
}
