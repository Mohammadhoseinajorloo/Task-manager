from typing import List

from backend.db.repository.tasks import create_new_task, delete_task, list_tasks, retrieve_task, update_task
from backend.db.session import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from backend.schemas.tasks import CreateTask, ShowTask, UpdateTask
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/tasks", response_model=ShowTask, status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTask, db: Session = Depends(get_db)):
    task = create_new_task(task=task, db=db, owner_id=1)
    return task


@router.get("/task/{id}", response_model=ShowTask)
async def get_task(id: int, db: Session = Depends(get_db)):
    task = retrieve_task(db=db, id=id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.get("/tasks", response_model=List[ShowTask])
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = list_tasks(db=db)
    return tasks


@router.put("/task/{id}", response_model=ShowTask)
async def get_task(id: int, task: UpdateTask, db: Session = Depends(get_db)):
    task = update_task(id=id, task=task, owner_id=1, db=db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/task/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    massage = delete_task(id=id, owner_id=1, db=db)
    if massage.get("error"):
        raise HTTPException(
            detail=massage.get("error"),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return {"msg": f"Successfully deleted task {id}"}
