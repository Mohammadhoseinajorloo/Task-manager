from backend.db.repository.user import create_new_user
from backend.schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_random_user(db: Session):
    user = UserCreate(email="mohammadhoseinajoloo76@gmail.com", username="mohammad", password="12345678")
    user = create_new_user(user=user, db=db)
    return user
