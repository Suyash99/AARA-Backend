from pydantic import BaseModel, EmailStr
from typing import Optional
class UserResponse(BaseModel):
    id: int
    username: str
    user_code: str
    email: EmailStr
    password: str
    colour_code: str
    user_photo_bytes: str
    created_at: Optional[int]
    updated_at: Optional[int]