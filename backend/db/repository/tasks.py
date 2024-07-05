from ..models.task import Task
from schemas.task import CreateTask, UpdateTask
from sqlalchemy.orm import Session


def create_new_task(task: CreateTask, db: Session, owner_id: int = 1) -> Task:
    task = Task(**task.dict(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def retrieve_task(id: int, db: Session):
    task = db.query(Task).filter(Task.id == id).first()
    return task


def list_tasks(db: Session):
    tasks = db.query(Task).filter(Task.is_active == True).all()
    return tasks


def update_task(id: int, task: UpdateTask, owner_id: int, db: Session):
    task_in_db = db.query(Task).filter(Task.id == id).first()
    if not task:
        return
    task_in_db.title = task.title
    task_in_db.description = task.description
    db.add(task_in_db)
    db.commit()
    return task_in_db


def delete_task(id: int, owner_id: int, db: Session):
    task_in_db = db.query(Task).filter(Task.id == id)
    if not task_in_db.first():
        return {"error": f"cannot find task with id: {id}"}
    task_in_db.delete()
    db.commit()
    return {"massage": f"deleted task with id: {id}"}
