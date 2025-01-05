from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ServerResponse(BaseModel, Generic[T]):
    is_success: bool
    status_code: int
    error_messages: Optional[List]
    error_message: Optional[str]
    payload: Optional[T] = None

    model_config = {}