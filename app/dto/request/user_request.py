from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    code: str
    name: str
    gemini_api_key: Optional[str]
    username: Optional[str]
    password: Optional[str]
    color: Optional[str]
    about: Optional[str]
