from objectbox import Id, Int64
from typing import Optional
class BaseModel:
    id = Id
    created_at = Int64
    updated_at = Int64
