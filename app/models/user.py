from objectbox import Entity, String, Date
from typing import Optional
from app.models.baseModel import BaseModel
from datetime import datetime
from pydantic import EmailStr

@Entity()
class User(BaseModel):
    username=String
    user_code=String
    email=String
    password=String
    colour_code=String
    user_photo_bytes=String
