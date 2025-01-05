from pydantic import BaseModel

class UserRequest(BaseModel):
    code: str

    username: str
    password: str

    name: str
    color: str
    about: str
