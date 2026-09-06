import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import type { ThreeElements } from '@react-three/fiber'
import { Mesh, MeshStandardMaterial, DoubleSide } from 'three'
import { useAssetSettings } from './AssetContext'
export type DGAssetProps=Omit<ThreeElements['group'],'ref'> & {instanceId?:string}
export interface NamedAssetProps extends DGAssetProps {asset:string}
const LITE_SHADOW_ASSETS=new Set(['WallPanel','StructuralColumn','Workbench','ReceptionDesk','ConferenceTable','Sofa','ServerRack','Planter','SessionFigure'])
/** Real textured GLB. Geometry, textures, and materials are shared by repeated instances.
 * Meters, Y-up. Mounted signs/displays use their center; furniture uses ground level.
 */
export function DGAsset({asset,instanceId,...props}:NamedAssetProps){
 const settings=useAssetSettings(),{scene}=useGLTF(`${settings.basePath}/${asset}.glb`)
 const object=useMemo(()=>{
  const object=scene.clone(true)
  object.traverse(node=>{if(node instanceof Mesh)node.userData={...node.userData,asset,instanceId:instanceId??asset}})
  return object
 },[scene,asset,instanceId])
 useEffect(()=>{
  const castAsset=settings.shadowMode==='full'||(settings.shadowMode==='lite'&&LITE_SHADOW_ASSETS.has(asset)),seen=new Set<MeshStandardMaterial>()
  object.traverse(node=>{
   if(!(node instanceof Mesh))return
   const name=node.name.toLowerCase(),glass=name.includes('glass'),decal=name.includes('wordmark')||name.includes('floormark')
   node.visible=settings.glass||!glass
   node.castShadow=castAsset&&!glass&&!decal
   node.receiveShadow=settings.shadowMode!=='off'&&!glass&&!decal
   const mats=Array.isArray(node.material)?node.material:[node.material]
   mats.forEach(material=>{
    const m=material as MeshStandardMaterial
    if(seen.has(m))return;seen.add(m)
    m.wireframe=settings.wireframe
    if('emissiveIntensity' in m)m.emissiveIntensity=m.name.startsWith('Screen_')?1.7:settings.emission
    if(m.transparent){m.depthWrite=false;m.side=DoubleSide}
   })
  })
 },[object,asset,settings.wireframe,settings.glass,settings.emission,settings.shadowMode])
 return <group {...props} name={instanceId??asset} userData={{asset,instanceId}}><primitive object={object} dispose={null}/></group>
}
