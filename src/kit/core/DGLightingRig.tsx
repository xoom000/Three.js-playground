import { Environment, Lightformer } from '@react-three/drei'
export interface LightingProps{mobile?:boolean;mode?:'cinematic'|'inspection'}
/** Emissive fixtures need a companion lighting rig. No external HDRI or hidden web requests. */
export function DGLightingRig({mobile=false,mode='cinematic'}:LightingProps){
 const inspection=mode==='inspection'
 return <>
  <hemisphereLight args={['#bed5d4','#172624',inspection?1.2:.52]}/>
  <spotLight position={[-3.6,7,3.5]} angle={.72} penumbra={1} intensity={inspection?155:120} color="#ffe0b3" castShadow shadow-mapSize={[mobile?1024:2048,mobile?1024:2048]} shadow-bias={-.0001} shadow-normalBias={.02}/>
  <spotLight position={[4,7,1]} angle={.78} penumbra={1} intensity={inspection?120:75} color="#d1e7eb" castShadow={!mobile} shadow-mapSize={[1024,1024]} shadow-bias={-.0001} shadow-normalBias={.02}/>
  <pointLight position={[1.5,2.4,-3.4]} color="#42d4e4" intensity={inspection?6:18} distance={8} decay={2}/>
  <pointLight position={[3.5,2.4,-3.4]} color="#d83bad" intensity={inspection?4:17} distance={7} decay={2}/>
  <pointLight position={[-3.0,2.6,3.6]} color="#ffcb8b" intensity={13} distance={7} decay={2}/>
  <pointLight position={[-4.3,2.4,-1.8]} color="#ffd4a0" intensity={8} distance={5} decay={2}/>
  <Environment resolution={mobile?64:128} frames={1} environmentIntensity={inspection?.9:.72}>
   <Lightformer intensity={3.6} position={[0,5,0]} rotation={[Math.PI/2,0,0]} scale={[11,8,1]} color="#ddd5c6"/>
   <Lightformer intensity={2.5} position={[7,2,4]} rotation={[0,-Math.PI/2,0]} scale={[10,3,1]} color="#9bbbc8"/>
   <Lightformer intensity={2} position={[-5,3,2]} rotation={[0,Math.PI/2,0]} scale={[6,3,1]} color="#e4b98e"/>
  </Environment>
 </>
}
