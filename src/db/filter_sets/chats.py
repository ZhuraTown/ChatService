from db.orm import User, Message, ChatParticipants
from sqlalchemy_filterset import (
    BaseFilterSet, SearchFilter, InFilter, Filter
)


class ChatsFilterSet(BaseFilterSet):
    search = SearchFilter(User.name, User.email)
    email__in = InFilter(User.email)
    name__in = InFilter(User.name)
    id__in = InFilter(User.id)


class MessageChatsFilterSet(BaseFilterSet):
    search = SearchFilter(Message.content)


class ChatParticipantsFilterSet(BaseFilterSet):
    chat_id = Filter(ChatParticipants.chat_id)
    user_id__in = InFilter(ChatParticipants.chat_id)
