from typing import List

from backend.apis.v1.route_login import get_current_user
from backend.db.models.user import User
from backend.db.repository.tasks import create_new_task, delete_task, list_tasks, retrieve_task, update_task
from backend.db.session import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from backend.schemas.tasks import CreateTask, ShowTask, UpdateTask
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/tasks", response_model=ShowTask, status_code=status.HTTP_201_CREATED)
async def create_task(
        task: CreateTask,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = create_new_task(task=task, db=db, owner_id=current_user.id)
    return task


@router.get("/task/{id}", response_model=ShowTask)
async def get_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = retrieve_task(task_id=task_id, db=db)
    if not task:
        raise HTTPException(
            detail=f"Task with ID {task.task_id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return task


@router.get("/tasks", response_model=List[ShowTask])
async def get_all_tasks(
        db: Session = Depends(get_db)
):
    tasks = list_tasks(db=db)
    return tasks


@router.put("/task/{id}", response_model=ShowTask)
async def update_a_task(
        task_id: int,
        task: UpdateTask,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = update_task(id=task_id, task=task, owner_id=current_user.id, db=db)
    if isinstance(task, dict):
        raise HTTPException(
            detail=task.get("error"),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return task


@router.delete("/task/{id}")
async def delete_a_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    massage = delete_task(id=task_id, owner_id=current_user.id, db=db)
    if massage.get("error"):
        raise HTTPException(
            detail=massage.get("error"),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return {"msg": f"Successfully deleted task {id}"}
