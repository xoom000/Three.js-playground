import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import type { ThreeElements } from '@react-three/fiber'
import { Mesh, Material, MeshStandardMaterial, DoubleSide } from 'three'
import { useAssetSettings } from './AssetContext'
export type DGAssetProps=Omit<ThreeElements['group'],'ref'> & {instanceId?:string}
export interface NamedAssetProps extends DGAssetProps {asset:string}
/** Real textured GLB, with geometry/textures cached and materials isolated per instance.
 * Meters, Y-up. Mounted signs/displays use their center; furniture uses ground level.
 */
export function DGAsset({asset,instanceId,...props}:NamedAssetProps){
 const settings=useAssetSettings(),{scene}=useGLTF(`${settings.basePath}/${asset}.glb`)
 const {object,materials}=useMemo(()=>{
  const object=scene.clone(true),clones=new Map<Material,Material>()
  object.traverse(node=>{
   if(!(node instanceof Mesh))return
   const name=node.name.toLowerCase(),glass=name.includes('glass'),decal=name.includes('wordmark')||name.includes('floormark')
   node.castShadow=!glass&&!decal;node.receiveShadow=!glass&&!decal
   const isolate=(original:Material)=>{
    let m=clones.get(original)
    if(!m){m=original.clone();clones.set(original,m)}
    return m
   }
   node.material=Array.isArray(node.material)?node.material.map(isolate):isolate(node.material)
   node.userData={...node.userData,asset,instanceId:instanceId??asset}
  })
  return {object,materials:[...clones.values()]}
 },[scene,asset,instanceId])
 useEffect(()=>{
  object.traverse(node=>{if(node instanceof Mesh)node.visible=settings.glass||!node.name.toLowerCase().includes('glass')})
  materials.forEach(material=>{
   const m=material as MeshStandardMaterial;m.wireframe=settings.wireframe
   if('emissiveIntensity' in m)m.emissiveIntensity=m.name.startsWith('Screen_')?1.7:settings.emission
   if(m.transparent){m.depthWrite=false;m.side=DoubleSide}
   m.needsUpdate=true
  })
 },[object,materials,settings.wireframe,settings.glass,settings.emission])
 useEffect(()=>()=>materials.forEach(m=>m.dispose()),[materials])
 return <group {...props} name={instanceId??asset} userData={{asset,instanceId}}><primitive object={object} dispose={null}/></group>
}
