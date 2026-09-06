import {useMemo,useEffect} from 'react'
import {MeshReflectorMaterial,useTexture} from '@react-three/drei'
import {RepeatWrapping,SRGBColorSpace} from 'three'
/** Optional planar reflection. The tile kit remains separate and independently exportable. */
export function ReflectiveFloor({width=10.8,depth=9.6,resolution=256}:{width?:number;depth?:number;resolution?:number}){
 const base=useTexture('./textures/DarkConcrete_color.jpg')
 const texture=useMemo(()=>{const t=base.clone();t.wrapS=t.wrapT=RepeatWrapping;t.repeat.set(width/2.4,depth/2.4);t.colorSpace=SRGBColorSpace;t.needsUpdate=true;return t},[base,width,depth])
 useEffect(()=>()=>texture.dispose(),[texture])
 return <mesh position={[0,.003,.6]} rotation={[-Math.PI/2,0,0]} receiveShadow>
  <planeGeometry args={[width,depth]}/><MeshReflectorMaterial map={texture} color="#a0a29a" resolution={resolution} blur={[200,70]} mixBlur={1} mixStrength={.55} mirror={.24} roughness={.40} metalness={.10} depthScale={.15} minDepthThreshold={.7} maxDepthThreshold={1}/>
 </mesh>
}
