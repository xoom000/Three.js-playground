import {RoomLayout,type RoomLayoutProps} from './RoomLayout'
import {layouts} from '../../layouts'
export function LobbyScene(props:Omit<RoomLayoutProps,'items'>){return <RoomLayout items={layouts.Lobby} {...props}/>}
