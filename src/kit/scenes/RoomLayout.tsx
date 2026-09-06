import {useMemo,useLayoutEffect,useRef} from 'react'
import {useGLTF} from '@react-three/drei'
import {useThree,type ThreeEvent} from '@react-three/fiber'
import {InstancedMesh,Mesh,MeshStandardMaterial,Matrix4,Object3D} from 'three'
import {useAssetSettings} from '../core/AssetContext'
import {libraryMaterial,isGlazing,castsShadow,receivesShadow} from '../core/materials'
export interface LayoutItem{id:string;asset:string;position:[number,number,number];rotation:[number,number,number];scale:number}
export interface RoomLayoutProps{items:LayoutItem[];onSelect?:(item:LayoutItem)=>void;showFigures?:boolean;hideFacade?:boolean}
const frontage=new Set(['GlassBay','WideGlassBay','GlassCorner','GlassDoor','DoubleGlassDoor','EntrancePortal','FacadeHeader','GlassDecal'])
function OpaqueBatch({source,items,onSelect}:{source:Mesh;items:LayoutItem[];onSelect?:RoomLayoutProps['onSelect']}){
 const settings=useAssetSettings(),ref=useRef<InstancedMesh>(null),invalidate=useThree(s=>s.invalidate)
 const material=libraryMaterial(source.material as MeshStandardMaterial,settings)
 useLayoutEffect(()=>{
  const mesh=ref.current;if(!mesh)return
  const transform=new Object3D(),matrix=new Matrix4()
  items.forEach((item,index)=>{transform.position.set(...item.position);transform.rotation.set(...item.rotation);transform.scale.setScalar(item.scale);transform.updateMatrix();matrix.multiplyMatrices(transform.matrix,source.matrixWorld);mesh.setMatrixAt(index,matrix)})
  mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingBox();mesh.computeBoundingSphere();invalidate()
 },[source,items,invalidate])
 return <instancedMesh ref={ref} args={[source.geometry,material,items.length]} name={`batch:${items[0].asset}:${source.name}`} castShadow={castsShadow(items[0].asset,material,settings.shadowMode)} receiveShadow={receivesShadow(material,settings.shadowMode)} dispose={null} onClick={onSelect?(e:ThreeEvent<MouseEvent>)=>{if(e.instanceId===undefined)return;e.stopPropagation();onSelect(items[e.instanceId])}:undefined}/>
}
function AssetBatch({asset,items,onSelect}:RoomLayoutProps&{asset:string}){
 const settings=useAssetSettings(),{scene}=useGLTF(`${settings.basePath}/${asset}.glb`)
 const parts=useMemo(()=>{scene.updateMatrixWorld(true);const meshes:Mesh[]=[];scene.traverse(o=>{if(o instanceof Mesh)meshes.push(o)});return meshes},[scene])
 return <group name={`asset:${asset}`}>{parts.map(part=>{
  const m=libraryMaterial(part.material as MeshStandardMaterial,settings)
  if(isGlazing(m)&&!settings.glass)return null
  if(!m.transparent)return <OpaqueBatch key={part.uuid} source={part} items={items} onSelect={onSelect}/>
  // Thin transparent panes stay independent for depth sorting. Do not instance
  // glass together: it can introduce incorrect alpha ordering while orbiting.
  return items.map(item=><group key={`${part.uuid}:${item.id}`} position={item.position} rotation={item.rotation} scale={item.scale}><mesh name={item.id} matrix={part.matrixWorld} matrixAutoUpdate={false} geometry={part.geometry} material={m} dispose={null} onClick={onSelect?e=>{e.stopPropagation();onSelect(item)}:undefined}/></group>)
 })}</group>
}
/** Modular authoring, GPU-instanced opaque repetitions. Picking retains item IDs. */
export function RoomLayout({items,onSelect,showFigures=true,hideFacade=false}:RoomLayoutProps){
 const batches=useMemo(()=>{
  const groups=new Map<string,LayoutItem[]>()
  for(const item of items){if(!showFigures&&item.asset==='SessionFigure'||hideFacade&&frontage.has(item.asset))continue;const group=groups.get(item.asset)??[];group.push(item);groups.set(item.asset,group)}
  return [...groups]
 },[items,showFigures,hideFacade])
 return <group name="DG_ModularRoom">{batches.map(([asset,instances])=><AssetBatch key={asset} asset={asset} items={instances} onSelect={onSelect}/>)}</group>
}
