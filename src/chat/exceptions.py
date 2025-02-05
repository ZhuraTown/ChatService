from dataclasses import dataclass

from fastapi import WebSocketException, status


@dataclass
class IncorrectSchemaException(WebSocketException):
    code: int = status.WS_1007_INVALID_FRAME_PAYLOAD_DATA
    reason: str = "Invalid data"
