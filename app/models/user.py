from objectbox import Entity, String, Id
from app.models.base_model import BaseModel


@Entity()
class User(BaseModel):
    id = Id()
    # Credentials
    username = String()
    password = String()

    # Details
    code = String()
    name = String()
    about = String()
    color = String()
    image_uri = String()

    # Gemini
    gemini_api_key = String()
