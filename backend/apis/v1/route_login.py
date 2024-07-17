import os

from backend.core.hashing import Hasher
from backend.core.security import create_access_token
from backend.db.repository.login import get_user
from backend.db.session import get_db
from backend.db.models.user import User
from backend.db.repository.profile import add_profile
from backend.core.upload_profile import save_profile
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, responses
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from backend.schemas.token import Token
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from backend.core.config import settings

router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=username, db=db)
    if not user:
        raise credentials_exception
    return user


@router.post("/upload-profile-image")
async def upload_profile_image(
        request: Request,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    save_name = save_profile(current_user.user_id, file)
    add_profile(save_name, current_user, db)
    return responses.RedirectResponse(
        f"/?alert=image upload success",
        status_code=status.HTTP_200_OK,
    )
