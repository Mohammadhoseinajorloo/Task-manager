from db.repository.user import create_new_user
from schemas.user import CreateUser
from sqlalchemy.orm import Session


def create_random_user(db: Session):
    user = CreateUser(email="mohammadhoseinajoloo76@gmail.com", username="mohammad", password="12345678")
    user = create_new_user(user=user, db=db)
    return user
