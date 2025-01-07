from pydantic import BaseModel

class RegenerateAuthRequest(BaseModel):
    username: str
    password: str
