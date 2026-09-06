import {DoubleSide,MeshStandardMaterial,Texture} from 'three'
import type {AssetSettings} from './AssetContext'

// Library materials are authored in tools/geometry.py. Keep one runtime material
// per authored name, so identical embedded maps are uploaded to the GPU once.
const shared=new Map<string,MeshStandardMaterial>()
const srgb:Record<string,string>={BlackenedSteel:'#252d30',BrushedHardware:'#8b9596',Rubber:'#111716',WarmPaper:'#b5ae9b',AgedBrass:'#897049',BranchBark:'#615338',Foliage0:'#344a2d',Foliage1:'#536a3b',Foliage2:'#6b7a45',Foliage3:'#3e5832',SkinNeutral:'#aa917b',Hair:'#272624',DGGreen:'#40d6a4',DataCyan:'#64dceb',SignalMagenta:'#bd349e',WarmWhiteDiffuser:'#ffddaa'}
const emitters=new Set(['DGGreen','DataCyan','SignalMagenta','WarmWhiteDiffuser','DGIdentity','Wordmark'])
export function libraryMaterial(original:MeshStandardMaterial,settings:AssetSettings){
 const key=original.name||original.uuid
 let m=shared.get(key)
 if(!m){
  m=original.clone()
  // Fix the kit exporter: CSS/sRGB swatches were written directly as linear
  // glTF factors. Textured materials are already decoded as sRGB by GLTFLoader.
  if(srgb[m.name])m.color.set(srgb[m.name])
  if(m.name==='DarkConcrete'){m.color.set('#a0a6a5');m.roughness=.94;m.metalness=.6;m.normalScale.set(.55,.55)}
  if(m.name==='GraphiteLaminate')m.color.set('#9caaa7')
  if(m.name==='Powdercoat')m.color.set('#a8b3b4')
  if(m.name==='GraphiteWoven')m.color.set('#777974')
  if(m.name==='BlackMarble')m.roughness=.95
  for(const texture of [m.map,m.normalMap,m.roughnessMap,m.metalnessMap,m.emissiveMap])if(texture instanceof Texture)texture.anisotropy=4
  if(m.transparent){m.depthWrite=false;m.side=DoubleSide;m.forceSinglePass=true}
  if(m.name.includes('Wordmark')||m.name==='FloorMark'){m.polygonOffset=true;m.polygonOffsetFactor=-2;m.polygonOffsetUnits=-2}
  if(m.name==='SmokedArchitecturalGlass'){m.color.set('#74958c');m.opacity=.14;m.roughness=.15}
  if(m.name==='CabinetGlass'){m.color.set('#49605a');m.opacity=.23}
  shared.set(key,m)
 }
 const wireChanged=m.wireframe!==settings.wireframe
 m.wireframe=settings.wireframe
 if(m.name.startsWith('Screen_'))m.emissiveIntensity=1.2
 else if(emitters.has(m.name))m.emissiveIntensity=settings.emission
 else m.emissiveIntensity=0
 if(wireChanged)m.needsUpdate=true
 return m
}
export function isGlazing(m:MeshStandardMaterial){return m.name==='SmokedArchitecturalGlass'||m.name==='CabinetGlass'}
export function castsShadow(asset:string,material:MeshStandardMaterial,mode:AssetSettings['shadowMode']){
 // Floor tiles must not shadow their neighbours at millimetre bevel boundaries.
 if(mode==='off'||material.transparent||material.name.startsWith('Screen_')||['FloorTile','FloorPlinth','Rug','FloorLabel','LinearLight','WallSconce'].includes(asset))return false
 return mode==='full'||['WallPanel','StructuralColumn','Workbench','ReceptionDesk','ConferenceTable','Sofa','OfficeChair','ServerRack','Planter','SessionFigure'].includes(asset)
}
export function receivesShadow(m:MeshStandardMaterial,mode:AssetSettings['shadowMode']){return mode!=='off'&&!m.transparent&&!m.name.startsWith('Screen_')}
