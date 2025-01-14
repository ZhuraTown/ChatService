from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated

from starlette.websockets import WebSocket

from db.orm import User
from users.dependency import get_current_user

router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='templates')

#
# active_connections: Dict[int, WebSocket] = {}
#
#
# # Функция для отправки сообщения пользователю, если он подключен
# async def notify_user(user_id: int, message: dict):
#     """Отправить сообщение пользователю, если он подключен."""
#     if user_id in active_connections:
#         websocket = active_connections[user_id]
#         # Отправляем сообщение в формате JSON
#         await websocket.send_json(message)


# todo: add route create group  chat
# todo: add route create direct chat
# todo: add route

@router.websocket('/')
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        await websocket.send_json({"message": "Message received!"})


#
# @router.get("/messages/{user_id}", response_model=List[MessageRead])
# async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
#     return await MessagesDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []
#
#
# @router.post("/messages", response_model=MessageCreate)
# async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
#     # Добавляем новое сообщение в базу данных
#     await MessagesDAO.add(
#         sender_id=current_user.id,
#         content=message.content,
#         recipient_id=message.recipient_id
#     )
#     # Подготавливаем данные для отправки сообщения
#     message_data = {
#         'sender_id': current_user.id,
#         'recipient_id': message.recipient_id,
#         'content': message.content,
#     }
#     # Уведомляем получателя и отправителя через WebSocket
#     await notify_user(message.recipient_id, message_data)
#     await notify_user(current_user.id, message_data)
#
#     # Возвращаем подтверждение сохранения сообщения
#     return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}
#
#
# @router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: int):
#     await websocket.accept()  # Принимаем соединение
#     active_connections[user_id] = websocket  # Сохраняем соединение пользователя
#     try:
#         while True:
#             await asyncio.sleep(1)  # Поддерживаем соединение активным
#     except WebSocketDisconnect:
#         active_connections.pop(user_id, None)  # Удаляем пользователя при отключении
#
