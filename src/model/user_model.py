from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int]
    username: str = Field(..., min_length=3)
    password: Optional[str]
