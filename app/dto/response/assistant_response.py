from pydantic import BaseModel
from typing import Optional

class AssistantResponse(BaseModel):
    name: str
    code: str
    temperature: float
    systemPrompt: str
    contextPrompt: str
    color: str
    edgeVoice: str
    edgePitch: int
    rvcVoice: str
    about: Optional[str]
    imageUri: Optional[str]

    class Config:
        arbitrary_types_allowed = True
