import enum


class ChatType(str, enum.Enum):
    DIRECT = "direct"
    GROUP = "group"


class EventType(str, enum.Enum):
    SEND_MESSAGE = "SEND_MESSAGE"
    LIST_MESSAGES = "LIST_MESSAGES"
    DELETE_MESSAGE = "DELETE_MESSAGE"
    UPDATE_MESSAGE = "UPDATE_MESSAGE"
