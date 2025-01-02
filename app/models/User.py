from objectbox import Entity
from app.models.BaseModel import BaseModel
from typing import Optional

@Entity
class User(BaseModel):
    username: str
    user_code: str
    email: str
    password: str
    colour_code: str
    user_photo_bytes: Optional[bytearray] = None
