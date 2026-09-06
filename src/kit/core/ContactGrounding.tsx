import {useMemo,useLayoutEffect,useRef,useEffect} from 'react'
import {CanvasTexture,InstancedMesh,MeshBasicMaterial,PlaneGeometry,Object3D} from 'three'
import {useThree} from '@react-three/fiber'
import type {LayoutItem} from '../scenes/RoomLayout'
const footprints:Record<string,[number,number]>={Workbench:[2.8,.94],ReceptionDesk:[3.7,1.1],ConferenceTable:[4.6,1.5],OfficeChair:[.66,.66],Sofa:[2.6,.85],Planter:[.56,.56],ServerRack:[.75,.88],SideCabinet:[1.7,.53],Bookcase:[1.1,.5],SessionFigure:[.55,.45]}
/** Cheap soft contact-darkening, not a claim of baked global illumination. */
export function ContactGrounding({items,showFigures=true}:{items:LayoutItem[];showFigures?:boolean}){
 const ref=useRef<InstancedMesh>(null),invalidate=useThree(s=>s.invalidate)
 const visible=useMemo(()=>items.filter(i=>footprints[i.asset]&&(showFigures||i.asset!=='SessionFigure')),[items,showFigures])
 const [geometry,material]=useMemo(()=>{
  const canvas=document.createElement('canvas');canvas.width=canvas.height=64
  const ctx=canvas.getContext('2d')!;const gradient=ctx.createRadialGradient(32,32,2,32,32,32);gradient.addColorStop(0,'rgba(0,0,0,.30)');gradient.addColorStop(.4,'rgba(0,0,0,.20)');gradient.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=gradient;ctx.fillRect(0,0,64,64)
  return [new PlaneGeometry(1,1),new MeshBasicMaterial({map:new CanvasTexture(canvas),transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-1,toneMapped:false})] as const
 },[])
 useLayoutEffect(()=>{
  if(!ref.current)return;const o=new Object3D()
  visible.forEach((i,n)=>{const [w,d]=footprints[i.asset];o.position.set(i.position[0],.025,i.position[2]);o.rotation.set(-Math.PI/2,0,i.rotation[1]);o.scale.set(w*i.scale*1.4,d*i.scale*1.4,1);o.updateMatrix();ref.current!.setMatrixAt(n,o.matrix)})
  ref.current.instanceMatrix.needsUpdate=true;ref.current.computeBoundingSphere();invalidate()
 },[visible,invalidate])
 useEffect(()=>()=>{geometry.dispose();material.map?.dispose();material.dispose()},[geometry,material])
 return <instancedMesh ref={ref} args={[geometry,material,visible.length]} renderOrder={1} name="contact-grounding"/>
}
