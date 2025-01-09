from pydantic import BaseModel
from typing import Optional
from app.utils.enums import MessageSenderType, MessageType

class MessageRequest(BaseModel):
    gid: Optional[int]
    quotedId: Optional[int]
    content: str
    timestamp: int
    sender: MessageSenderType
    type: MessageType
    chatCode: str
