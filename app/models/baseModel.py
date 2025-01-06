from objectbox import Int64, Int32, String

class BaseModel:
    version = Int32()
    created_at = Int64()
    updated_at = Int64()
    created_by = String()
    updated_by = String()
