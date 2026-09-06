import {useEffect} from 'react'
import {useThree} from '@react-three/fiber'
/** Resolve sharply at rest; lower only pixel cost during camera motion. MSAA stays on. */
export function ViewportQuality({mobile,quality}:{mobile:boolean;quality:'balanced'|'high'}){
 const {controls,setDpr,invalidate}=useThree()
 useEffect(()=>{
  const native=window.devicePixelRatio||1,rest=Math.min(native,quality==='high'?2:1.75),moving=Math.min(native,quality==='high'?1.5:1.25)
  let timer:ReturnType<typeof setTimeout>|undefined
  const settle=()=>{setDpr(rest);invalidate()}
  const activity=()=>{setDpr(mobile?moving:rest);clearTimeout(timer);timer=setTimeout(settle,240)}
  const ctrl=controls as unknown as {addEventListener:(t:string,fn:()=>void)=>void;removeEventListener:(t:string,fn:()=>void)=>void}|null
  ctrl?.addEventListener('change',activity);settle()
  return()=>{clearTimeout(timer);ctrl?.removeEventListener('change',activity)}
 },[controls,mobile,quality,setDpr,invalidate]);return null
}
