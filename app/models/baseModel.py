from datetime import datetime
from objectbox import Id, Date
class BaseModel:
    id = Id
    created_at = Date(py_type=datetime)
    updated_at = Date(py_type=datetime)
