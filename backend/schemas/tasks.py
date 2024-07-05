from datetime import date
from typing import Optional

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None


class UpdateTask(BaseModel):
    pass


class ShowTask(BaseModel):
    title: str
    description: Optional[str]
    created_at: date

    class Config:
        orm_mode = True
