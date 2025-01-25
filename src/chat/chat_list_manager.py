from typing import TYPE_CHECKING

from starlette.websockets import WebSocket


if TYPE_CHECKING:
    from chat.service import ChatService


class ChatListConnectionManager:

    def __init__(self):
        self.online_users: list = []

    async def connect(self, websocket: WebSocket, chat_service: 'ChatService', user_id: int):
        await websocket.accept()
        await self.send_message(
            data={'unread_chats': await chat_service.list_chats_user(user_id)},
            status=1000,
            event='connect',
            websocket=websocket
        )

    async def disconnect(
            self,
            websocket: WebSocket,
            chat_service: 'ChatService'
    ):
        if chat_service:
            ...
            # self.online_users.remove((websocket, chat_service.current_user.uuid))
            # await chat_service.session.close()

    @staticmethod
    async def send_message(data: dict, status: int, event: str, websocket):
        data = {'status': status, 'data': data, 'event': event}
        await websocket.send_json(data)

    async def receive_message(self,
                              data: dict,
                              websocket: WebSocket,
                              chat_service: 'ChatService'):
        # try:
        #     event_message = EventChatListSchema.parse_raw(data)
        # except ValidationError as e:
        #     await self.send_message(data={'detail': f'Invalid json schema format for event'},
        #                             status=1007, event='error', websocket=websocket)
        #     logger.warning(f"Invalid json schema format was obtained from "
        #                    f"{chat_service.current_user.uuid}: {e}")
        # else:
        #     try:
        #         await getattr(self, f'event__{event_message.command}', self.method_undefined)(event_message.command,
        #                                                                                       event_message.payload,
        #                                                                                       websocket,
        #                                                                                       chat_service)
        #     except HTTPException as e:
            await self.send_message(
                data={'detail': e.detail},
                status=1007,
                event="error",
                websocket=websocket
            )