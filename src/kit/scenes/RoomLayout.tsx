import { DGAsset } from '../core/DGAsset'
export interface LayoutItem{id:string;asset:string;position:[number,number,number];rotation:[number,number,number];scale:number}
export interface RoomLayoutProps{items:LayoutItem[];onSelect?:(item:LayoutItem)=>void;showFigures?:boolean;hideFacade?:boolean}
/** Independent instance placement, not agent execution or filesystem state. */
export function RoomLayout({items,onSelect,showFigures=true,hideFacade=false}:RoomLayoutProps){
 const hidden=hideFacade?new Set(['GlassBay','WideGlassBay','GlassCorner','GlassDoor','DoubleGlassDoor','EntrancePortal','FacadeHeader','GlassDecal']):new Set<string>()
 return <group name="DG_ModularRoom">{items.filter(i=>(showFigures||i.asset!=='SessionFigure')&&!hidden.has(i.asset)).map(item=><DGAsset key={item.id} asset={item.asset} instanceId={item.id} position={item.position} rotation={item.rotation} scale={item.scale} onClick={onSelect?event=>{event.stopPropagation();onSelect(item)}:undefined}/>)}</group>
}
