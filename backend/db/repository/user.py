from core.hashing import Hasher
from ..models import User
from schemas.user import CreateUser
from sqlalchemy.orm import Session


def create_new_user(user: CreateUser, db: Session):
    user = User(
        email=user.email,
        username=user.username,
        password=Hasher.get_pass_hash(user.password),
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
