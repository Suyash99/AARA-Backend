from datetime import datetime
from objectbox.model import Entity
class BaseModel(Entity):
    id: int
    created_at: datetime
    updated_at: datetime
