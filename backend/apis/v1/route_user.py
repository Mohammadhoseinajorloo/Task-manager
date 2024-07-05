from backend.db.repository.user import create_new_user
from backend.db.session import get_db
from fastapi import APIRouter, Depends, status
from backend.schemas.user import ShowUser, UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
