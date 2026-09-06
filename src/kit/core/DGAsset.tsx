import {useLayoutEffect,useMemo} from 'react'
import {useGLTF} from '@react-three/drei'
import {useThree,type ThreeElements} from '@react-three/fiber'
import {Mesh,MeshStandardMaterial} from 'three'
import {useAssetSettings} from './AssetContext'
import {libraryMaterial,isGlazing,castsShadow,receivesShadow} from './materials'
export type DGAssetProps=Omit<ThreeElements['group'],'ref'> & {instanceId?:string}
export interface NamedAssetProps extends DGAssetProps{asset:string}
/** Independent exported component. Runtime sharing never changes the GLB file. */
export function DGAsset({asset,instanceId,...props}:NamedAssetProps){
 const settings=useAssetSettings(),{scene}=useGLTF(`${settings.basePath}/${asset}.glb`),invalidate=useThree(s=>s.invalidate)
 const object=useMemo(()=>scene.clone(true),[scene])
 useLayoutEffect(()=>{
  object.traverse(node=>{
   if(!(node instanceof Mesh))return
   const originals=Array.isArray(node.material)?node.material:[node.material]
   const materials=originals.map(m=>libraryMaterial(m as MeshStandardMaterial,settings))
   node.material=Array.isArray(node.material)?materials:materials[0]
   node.visible=settings.glass||!materials.every(isGlazing)
   node.castShadow=materials.some(m=>castsShadow(asset,m,settings.shadowMode))
   node.receiveShadow=materials.some(m=>receivesShadow(m,settings.shadowMode))
   node.userData={asset,instanceId:instanceId??asset}
  });invalidate()
 },[object,asset,instanceId,settings,invalidate])
 return <group {...props} name={instanceId??asset} userData={{asset,instanceId}}><primitive object={object} dispose={null}/></group>
}
