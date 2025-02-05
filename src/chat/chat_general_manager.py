from collections import defaultdict

from pydantic import ValidationError
from starlette.websockets import WebSocket
from fastapi import status

from chat.schemas import MessageSchema
from db.orm import User
from logger import logger


class ChatGeneralManager:

    def __init__(self):
        self.active_connections: dict = {}
        self.messages: list = []

    async def connect(
            self,
            websocket: WebSocket,
            current_user: User,
    ):
        await websocket.accept()
        self.active_connections[current_user.id] = (websocket, current_user)
        self.messages.append({"message": f"Hello {current_user.name}!", "author": "System"})
        last_messages = self.messages[-10:]
        data = {"messages": last_messages}
        await self._send_message(data, status=1000, websocket=websocket)

    @staticmethod
    async def _send_message(data: dict, status: int, websocket):
        data = {'status': status, 'data': data}
        await websocket.send_json(data)

    async def receive_message(self,
                              data: dict,
                              websocket: WebSocket
                              ):
        try:
            event_message: MessageSchema = MessageSchema.model_validate(data)
        except ValidationError as e:
            logger.warning(f"Invalid json schema format was obtained from: {e}")
            await self._send_message(
                data={'detail': f'Invalid json schema format for event'},
                status=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
                websocket=websocket
            )
        else:
            message = event_message.model_dump(mode='json')
            message['author'] = 'Some user'
            self.messages.append(message)
            await self.broadcast_message(message)

    async def broadcast_message(self, message: dict):
        for user_id, connection_data in self.active_connections.items():
            connection_data: [WebSocket, User]
            websocket, user = connection_data
            await self._send_message(message, status=1000, websocket=websocket)

    async def disconnect(self, current_user: User,  websocket: WebSocket):
        message = {"message": f"{current_user.name} bye-bye!", "author": "System"}
        self.messages.append(message)
        self.active_connections.pop(current_user.id, None)
        await self.broadcast_message(message)
