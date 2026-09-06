import {DefaultLoadingManager} from 'three'
import {createRoot} from 'react-dom/client'
import {App} from './App'
import './style.css'
declare global { interface Window { __DG_ASSETS__?:Record<string,string> } }
if(window.__DG_ASSETS__){const files=window.__DG_ASSETS__;DefaultLoadingManager.setURLModifier(url=>{const path=url.replace(/^\.\//,'');return files[path]??url})}
const el=document.getElementById('root');if(!el)throw new Error('Missing mount element')
createRoot(el).render(<App/> )
