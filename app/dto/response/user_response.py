from pydantic import BaseModel

class UserResponse(BaseModel):
    code: str
    name: str
    about: str
    color: str

    class Config:
        arbitrary_types_allowed = True

class UserResponseV2(UserResponse):
    password:str