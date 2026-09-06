import {RoomLayout,type RoomLayoutProps} from './RoomLayout'
import {layouts} from '../../layouts'
export function ResearchScene(props:Omit<RoomLayoutProps,'items'>){return <RoomLayout items={layouts.Research} {...props}/>}
