from pydantic import BaseModel
from typing import Optional
from app.utils.enums import ChatType

class ChatRequest(BaseModel):
    code: Optional[str]
    name: str
    type: ChatType
    imageUri: str
    password: str
    showSystemMessages: bool
    showFailedMessages: bool
    showCommands: bool
    showTokens: bool
    autoPlaybackAudio: bool
    autoResponses: bool
    ownerUserCode: str
    assistant_id: int
    user_id: int
