import { createContext, useContext } from 'react'
export type ShadowMode='full'|'lite'|'off'
export interface AssetSettings {basePath:string;wireframe:boolean;glass:boolean;emission:number;shadowMode:ShadowMode}
export const AssetContext=createContext<AssetSettings>({basePath:'./models',wireframe:false,glass:true,emission:2.8,shadowMode:'full'})
export const useAssetSettings=()=>useContext(AssetContext)
