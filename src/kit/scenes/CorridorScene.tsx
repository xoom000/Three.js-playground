import {RoomLayout,type RoomLayoutProps} from './RoomLayout'
import {layouts} from '../../layouts'
export function CorridorScene(props:Omit<RoomLayoutProps,'items'>){return <RoomLayout items={layouts.Corridor} {...props}/>}
