from objectbox import Entity
from Base import BaseModel

@Entity
class User(BaseModel):
    username: str
    user_code: str
    email: str
    password: str
    colour_code: str
