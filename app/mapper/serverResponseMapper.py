from typing import TypeVar, Generic, Dict, Optional
from pydantic import BaseModel
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class ServerResponse(BaseModel, Generic[T]):
    is_success: bool
    status_code: int
    error_message: str = ""  # Default empty string
    error_messages: Dict[str, str] = field(default_factory=dict)  # Default empty dict
    payload: Optional[T] = None  # Making payload optional with default None

    class Config:
        arbitrary_types_allowed = True