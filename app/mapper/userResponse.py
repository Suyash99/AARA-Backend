from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    username: str
    user_code: str
    email: EmailStr
    password: str
    colour_code: str
    user_photo_bytes: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]