from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    colour_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
