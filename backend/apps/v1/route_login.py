import json
import os

from fastapi.security import OAuth2PasswordBearer

from backend.apis.v1.route_login import authenticate_user
from backend.core.security import create_access_token
from backend.db.repository.user import create_new_user
from backend.db.session import get_db
from fastapi import APIRouter, Depends, Form, Request, responses, status
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from backend.schemas.user import UserCreate
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.get("/upload-profile-image")
async def upload_profile_image(request: Request):
    return templates.TemplateResponse("auth/upload_image.html", {"request": request})


@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register(
        request: Request,
        email: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    errors = []
    try:
        user = UserCreate(email=email, username=username, password=password)
        create_new_user(user=user, db=db)
        return responses.RedirectResponse(
            "/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND
        )
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0] + ": " + item.get("msg"))
        return templates.TemplateResponse(
            "auth/register.html", {"request": request, "errors": errors}
        )


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
):
    errors = []
    user = authenticate_user(email=email, password=password, db=db)
    if not user:
        errors.append("Invalid email or password")
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "error": errors}
        )
    access_token = create_access_token(data={"sub": email})
    response = responses.RedirectResponse(
        "/?alert=sucssesfuly%20logged", status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return response
