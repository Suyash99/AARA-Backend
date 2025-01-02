from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRequest(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    user_photo_bytes: Optional[bytearray] = None
    colour_code: str

    class Config:
        from_attributes = True
