from pydantic import BaseModel, validator


class UserResponse(BaseModel):
    code: str

    name: str
    about: str
    color: str
    image: bytearray

    class Config:
        arbitrary_types_allowed = True