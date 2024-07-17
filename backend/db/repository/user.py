import os

from backend.core.hashing import Hasher
from backend.db.models.user import User
from backend.schemas.user import UserCreate
from sqlalchemy.orm import Session
from backend.core.config import settings
from fastapi import UploadFile


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        username=user.username,
        password=Hasher.get_password_hash(user.password),
        profile=user.profile,
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
