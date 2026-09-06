import {RoomLayout,type RoomLayoutProps} from './RoomLayout'
import {layouts} from '../../layouts'
export function MeetingScene(props:Omit<RoomLayoutProps,'items'>){return <RoomLayout items={layouts.Meeting} {...props}/>}
