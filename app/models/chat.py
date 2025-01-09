from objectbox import Int64, Entity
from app.models.base_model import BaseModel

@Entity()
class Chat(BaseModel):
    assistant_id = Int64
    user_id = Int64
