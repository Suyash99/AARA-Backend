from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    code: str
    name: str
    username: Optional[str]
    password: Optional[str]
    color: Optional[str]
    about: Optional[str]
