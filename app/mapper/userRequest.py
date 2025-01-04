from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserRequest(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    user_photo_bytes: str
    colour_code: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(arbitrary_types_allowed=True)
