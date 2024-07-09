from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes: bool = True
