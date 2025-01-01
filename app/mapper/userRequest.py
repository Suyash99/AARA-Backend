from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    username: str
    user_code: str
    email: EmailStr
    password: str
    colour_code: str

    class Config:
        from_attributes = True
