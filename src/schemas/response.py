from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[dict] = None
