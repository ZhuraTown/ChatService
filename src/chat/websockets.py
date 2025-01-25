from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from chat.chat_list_manager import ChatListConnectionManager
from chat.dependency import get_chat_service
from chat.service import ChatService

router = APIRouter(
    prefix='/chat-list',
    tags=['chat']
)

manager = ChatListConnectionManager()


@router.websocket("")
async def websocket_chat_list(websocket: WebSocket,
                              chat_service: ChatService = Depends(get_chat_service)):
    try:
        if websocket.application_state != WebSocketState.DISCONNECTED:
            await manager.connect(websocket, chat_service)
            while True:
                data = await websocket.receive_text()
                await manager.receive_message(data, websocket, chat_service)

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.error(message)
        logger.warning("Disconnecting Websocket")

    finally:
        await manager.disconnect(websocket, chat_service)


# @router.websocket('/')
# async def chat(
#         websocket: WebSocket,
#
# ):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_json()
#         print(data)
#         await websocket.send_json({"message": "Message received!"})