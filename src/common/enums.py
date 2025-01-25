import enum


class ChatType(str, enum.Enum):
    DIRECT = "direct"
    GROUP = "group"


class ChatAction(str, enum.Enum):
    CREATE_CHAT = "create_chat"
    GET_CHAT = "get_chat"
    SEND_MESSAGE = "send_message"
    GET_CHAT_HISTORY = "get_chat_history"
