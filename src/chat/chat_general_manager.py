from collections import defaultdict

from pydantic import ValidationError
from starlette.websockets import WebSocket
from fastapi import status

from chat.schemas import EventSchema, ParticipantSchema, MessageRead
from chat.service import ChatService
from db.orm import User
from logger import logger


class ChatGeneralManager:
    system_author: str = "System"
    chat_id: int = 1

    def __init__(self):
        self.active_connections: dict = {}

    async def connect(
            self,
            websocket: WebSocket,
            current_user: User,
            chat_service: ChatService,
    ):
        await websocket.accept()
        participants = await chat_service.list_participants(self.chat_id)
        if current_user not in participants:
            await chat_service.create_participants(self.chat_id, [current_user.id])
            await chat_service.uow.commit()
            participants.append(current_user)
        self.active_connections[current_user.id] = (websocket, current_user)
        last_messages = await chat_service.list_messages(
            self.chat_id, limit=10, offset=0
        )
        data = {
            "messages": [MessageRead.parse_obj(m).model_dump(mode='json') for m in last_messages],
            "participants": [
                (ParticipantSchema.parse_obj(p)).model_dump(mode='json') for p in participants
            ]
        }
        await self._send_message(data, status=1000, websocket=websocket)

    @staticmethod
    async def _send_message(data: dict, status: int, websocket):
        data = {'status': status, 'data': data}
        await websocket.send_json(data)

    async def receive_message(self,
                              data: dict,
                              websocket: WebSocket,
                              user: User,
                              chat_service: ChatService
                              ):
        try:
            event_message: EventSchema = EventSchema.model_validate(data)
        except ValidationError as e:
            logger.warning(f"Invalid json schema format was obtained from: {e}")
            await self._send_message(
                data={'detail': f'Invalid json schema format for event'},
                status=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                websocket=websocket
            )
        else:
            message = await chat_service.create_message(
                self.chat_id, event_message.content, user.id
            )
            message.sender = user
            await self.broadcast_message(
                MessageRead.parse_obj(message).model_dump(mode='json')
            )

    async def broadcast_message(self, message: dict):
        for user_id, connection_data in self.active_connections.items():
            connection_data: [WebSocket, User]
            websocket, user = connection_data
            await self._send_message(message, status=1000, websocket=websocket)

    async def disconnect(self, current_user: User):
        self.active_connections.pop(current_user.id, None)
