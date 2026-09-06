import { createContext, useContext } from 'react'
export interface AssetSettings {basePath:string;wireframe:boolean;glass:boolean;emission:number}
export const AssetContext=createContext<AssetSettings>({basePath:'./models',wireframe:false,glass:true,emission:2.8})
export const useAssetSettings=()=>useContext(AssetContext)
