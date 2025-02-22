from datetime import datetime
from typing import Self, Optional

from pydantic import BaseModel, Field, model_validator, ValidationError, field_validator, ConfigDict

from common.enums import ChatType


class UserRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(extra="allow", from_attributes=True)

class MessageRead(BaseModel):
    id: int
    sender_id: int
    content: str
    created_at: datetime
    sender: UserRead
    model_config = ConfigDict(extra="allow", from_attributes=True)


class CreateChatSchemaRequest(BaseModel):
    type: ChatType
    participants: list[int] = Field(..., min_length=1)
    name: str | None = Field(None, min_length=1)
    about: str | None = Field(None, min_length=1)
    is_private: bool = Field(True)

    @model_validator(mode='after')
    def validate_type_and_participants(self) -> Self:
        if self.type.DIRECT and len(self.participants) > 1:
            raise ValueError('Личный чат, не может иметь больше 1 участника')
        if self.type.DIRECT and (self.name or self.about):
            raise ValueError("Переписка с пользователем, без названия чата об этом")
        return self


class AddParticipantsChatSchemaRequest(BaseModel):
    participants: list[int] = Field(..., min_length=1)

    @field_validator("participants")
    def type_unique(cls, value: list[int]):
        if len(value) != len(set(value)):
            raise ValueError("Переданы дубликаты")
        return value


class ChatResponseSchema(BaseModel):
    type: ChatType
    name: str | None
    created_at: datetime | None

    class Config:
        from_attributes = True


class ChatParticipantsFilters(BaseModel):
    chat_id: Optional[int] = None
    user_id__in: Optional[list[int]] = None


class EventSchema(BaseModel):
    content: str
    model_config = ConfigDict(extra="allow", from_attributes=True)


class ParticipantSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(extra="allow", from_attributes=True)

