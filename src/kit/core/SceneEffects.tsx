import {useEffect,useMemo} from 'react'
import {useFrame,useThree} from '@react-three/fiber'
import {Vector2} from 'three'
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js'
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js'
import {SSAOPass} from 'three/addons/postprocessing/SSAOPass.js'
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js'
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js'
export function SceneEffects({ao=true}:{ao?:boolean}){
 const {gl,scene,camera,size}=useThree()
 const composer=useMemo(()=>{
  const c=new EffectComposer(gl)
  if(ao){const s=new SSAOPass(scene,camera,512,512);s.kernelRadius=7;s.minDistance=.003;s.maxDistance=.055;c.addPass(s)}
  else c.addPass(new RenderPass(scene,camera))
  c.addPass(new UnrealBloomPass(new Vector2(512,512),.24,.25,1.05));c.addPass(new OutputPass());return c
 },[gl,scene,camera,ao])
 useEffect(()=>{composer.setSize(size.width,size.height)},[composer,size])
 useEffect(()=>()=>{composer.passes.forEach(p=>p.dispose());composer.dispose()},[composer])
 useFrame((_,delta)=>composer.render(delta),1)
 return null
}
