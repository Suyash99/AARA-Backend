from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    colour_code: str
    user_photo: Optional[bytes] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
