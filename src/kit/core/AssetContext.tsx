import {createContext,useContext} from 'react'
export interface AssetSettings{basePath:string;wireframe:boolean;glass:boolean;emission:number;shadowMode:'off'|'lite'|'full'}
export const AssetContext=createContext<AssetSettings>({basePath:'./models',wireframe:false,glass:true,emission:2,shadowMode:'lite'})
export const useAssetSettings=()=>useContext(AssetContext)
