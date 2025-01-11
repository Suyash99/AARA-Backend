from pydantic import BaseModel
from typing import Optional
from app.utils.enums import ChatType

class ChatResponse (BaseModel):
    code: Optional[str]
    name: str
    type: ChatType
    imageUri: str
