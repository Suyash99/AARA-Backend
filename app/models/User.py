from objectbox import Entity
from Base import BaseModel

@Entity
class User(BaseModel):
    username: str
    email: str
    password: str
    user_code: str
    colour_code: str
