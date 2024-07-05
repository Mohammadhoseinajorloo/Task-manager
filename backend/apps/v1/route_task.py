from typing import Optional

from apis.v1.route_login import get_current_user
from db.repository.task import create_new_task, delet_task, list_task, retreive_task
from db.session import get_db
from fastapi import APIRouter, Depends, Form, status, Request, responses
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.task import CreateTask
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/")
async def home(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    task = list_task(db=db)
    return templates.TemplateResponse(
        "/task/detail.html", {"request": request, "task": task, "alert": alert}
    )


@router.get("/app/task/{id}")
async def task_detail(request: Request, id: int, db: Session = Depends(get_db)):
    task = retreive_task(id=id, db=db)
    return templates.TemplateResponse(
        "/task/detail.html", {"request": request, "task": task}
    )


@router.get("/app/create_new_task")
async def create_new_task(request: Request):
    return templates.TemplateResponse("/task/create_new_task.html", {"request": request})


@router.post("/app/create_new_task")
async def create_new_task(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        owner = get_current_user(token=token, db=db)
        task = CreateTask(titel=title, description=description)
        task = create_new_task(task=task, db=db, owner_id=owner)
        return responses.RedirectResponse(
            "/?alert=task submited successfully", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        error = ["Please login to create a new task"]
        print("Exeption raised:", e)
        return templates.TemplateResponse(
            "/task/create_new_task.html",
            {"request": request, "error": error, "title": title, "description": description}
        )


@router.get("/delete/{id}")
async def delete_a_task(request: Request, id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        owner = get_current_user(token=token, db=db)
        msg = delet_task(id=id, owner_id=owner, db=db)
        alert = msg.get("error") or msg.get("alert")
        return responses.RedirectResponse(
            f"?alert={alert}", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        print(f"Exeption raised while deleting a task: {e}")
        task = retreive_task(id=id, db=db)
        return templates.TemplateResponse(
            "task/detail.html",
            {"request": request, "alert": "Please login Again", "task": task}
        )
