from db.repository.user create_new_user
from db.session import get_db
from fastapi import APIRouter, Depends, status
from schemas.user import ShowUser, CreateUser
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_users(user: CreateUser, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
