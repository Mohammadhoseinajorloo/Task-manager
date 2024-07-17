from backend.db.models.user import User
from sqlalchemy.orm import Session


def add_profile(save_name: str, current_user: User, db: Session):
    current_user.profile = save_name
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
