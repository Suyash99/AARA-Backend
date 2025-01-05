from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRequest(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    user_photo_bytes: str
    colour_code: str
    created_at: Optional[int]
    updated_at: Optional[int]
