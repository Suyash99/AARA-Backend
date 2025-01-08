from objectbox import Int64, Entity
from app.models.base_model import BaseModel

@Entity()
class Message(BaseModel):
    chat_id = Int64
    assistant_id = Int64
    user_id = Int64
