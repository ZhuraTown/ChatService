from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from chat.chat_general_manager import ChatGeneralManager
from chat.dependency import auth_user, get_chat_service
from chat.service import ChatService
from db.orm import User

router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

manager_general = ChatGeneralManager()

#
# @router.websocket("")
# async def websocket_chat_list(websocket: WebSocket,
#                               chat_service: ChatService = Depends(get_chat_service)):
#     try:
#         if websocket.application_state != WebSocketState.DISCONNECTED:
#             await manager.connect(websocket, chat_service)
#             while True:
#                 data = await websocket.receive_text()
#                 await manager.receive_message(data, websocket, chat_service)
#
#     except Exception as ex:
#         template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#         message = template.format(type(ex).__name__, ex.args)
#         logger.error(message)
#         logger.warning("Disconnecting Websocket")
#
#     finally:
#         await manager.disconnect(websocket, chat_service)


@router.websocket("/general")
async def general(
        websocket: WebSocket,
        current_user: Annotated[User, Depends(auth_user)],
        chat_service: Annotated[ChatService, Depends(get_chat_service)]
):
    await manager_general.connect(websocket, current_user, chat_service)
    try:
        while True:
            data = await websocket.receive_json()
            await manager_general.receive_message(data, websocket, current_user, chat_service)
    except WebSocketDisconnect:
        await manager_general.disconnect(current_user)