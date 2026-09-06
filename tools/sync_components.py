from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];cat=json.loads((r/'public/catalog.json').read_text());exports=[]
for a in cat:
 name=a['id'];p=r/f'src/kit/{a["category"]}/{name}.tsx';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(f'''import {{DGAsset,type DGAssetProps}} from '../core/DGAsset'\n/** {name}. Independent textured GLB. */\nexport function {name}(props:DGAssetProps){{return <DGAsset asset="{name}" {{...props}}/>}}\n''');exports.append(f"export {{{name}}} from './{a['category']}/{name}'")
(r/'src/kit/index.ts').write_text('\n'.join(exports)+"\nexport {DGAsset} from './core/DGAsset'\nexport type {DGAssetProps} from './core/DGAsset'\nexport {AssetContext} from './core/AssetContext'\nexport {DGLightingRig} from './core/DGLightingRig'\nexport {RoomLayout} from './scenes/RoomLayout'\n")
(r/'src/catalog.ts').write_text('export const catalog = '+json.dumps(cat,indent=2)+' as const\n')
layouts=json.loads((r/'public/layouts.json').read_text());(r/'src/layouts.ts').write_text('import type {LayoutItem} from "./kit/scenes/RoomLayout"\nexport const layouts: Record<string,LayoutItem[]> = '+json.dumps(layouts,indent=2)+'\n')
for name in layouts:
 (r/f'src/kit/scenes/{name}Scene.tsx').write_text(f'''import {{RoomLayout,type RoomLayoutProps}} from './RoomLayout'\nimport {{layouts}} from '../../layouts'\nexport function {name}Scene(props:Omit<RoomLayoutProps,'items'>){{return <RoomLayout items={{layouts.{name}}} {{...props}}/>}}\n''')
 with (r/'src/kit/index.ts').open('a') as f:f.write(f"export {{{name}Scene}} from './scenes/{name}Scene'\n")
