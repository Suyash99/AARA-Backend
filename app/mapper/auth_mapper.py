from pydantic import BaseModel

class RegenerateTokenRequest(BaseModel):
    username: str
    password: str
