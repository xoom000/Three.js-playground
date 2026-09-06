import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import type { ThreeElements } from '@react-three/fiber'
import { Mesh, Material, MeshStandardMaterial, DoubleSide } from 'three'
import { useAssetSettings } from './AssetContext'
export type DGAssetProps=Omit<ThreeElements['group'],'ref'> & {instanceId?:string}
export interface NamedAssetProps extends DGAssetProps {asset:string}
const LITE_SHADOW_ASSETS=new Set(['WallPanel','StructuralColumn','Workbench','ReceptionDesk','ConferenceTable','Sofa','ServerRack','Planter','SessionFigure'])
/** Real textured GLB, with geometry/textures cached and materials isolated per instance.
 * Meters, Y-up. Mounted signs/displays use their center; furniture uses ground level.
 */
export function DGAsset({asset,instanceId,...props}:NamedAssetProps){
 const settings=useAssetSettings(),{scene}=useGLTF(`${settings.basePath}/${asset}.glb`)
 const {object,materials}=useMemo(()=>{
  const object=scene.clone(true),clones=new Map<Material,Material>()
  object.traverse(node=>{
   if(!(node instanceof Mesh))return
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
  const castAsset=settings.shadowMode==='full'||(settings.shadowMode==='lite'&&LITE_SHADOW_ASSETS.has(asset))
  object.traverse(node=>{
   if(!(node instanceof Mesh))return
   const name=node.name.toLowerCase(),glass=name.includes('glass'),decal=name.includes('wordmark')||name.includes('floormark')
   node.visible=settings.glass||!glass
   node.castShadow=castAsset&&!glass&&!decal
   node.receiveShadow=settings.shadowMode!=='off'&&!glass&&!decal
  })
  materials.forEach(material=>{
   const m=material as MeshStandardMaterial;m.wireframe=settings.wireframe
   if('emissiveIntensity' in m)m.emissiveIntensity=m.name.startsWith('Screen_')?1.7:settings.emission
   if(m.transparent){m.depthWrite=false;m.side=DoubleSide}
   m.needsUpdate=true
  })
 },[object,materials,asset,settings.wireframe,settings.glass,settings.emission,settings.shadowMode])
 useEffect(()=>()=>materials.forEach(m=>m.dispose()),[materials])
 return <group {...props} name={instanceId??asset} userData={{asset,instanceId}}><primitive object={object} dispose={null}/></group>
}
