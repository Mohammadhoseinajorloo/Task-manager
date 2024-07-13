import json
from datetime import datetime

from backend.db.models.task import Task
from backend.schemas.tasks import CreateTask, UpdateTask
from backend.cache.logic.cache import cache_get, cache_set
from backend.cache.connection import cache
from sqlalchemy.orm import Session


def create_new_task(task: CreateTask, db: Session, owner_id: int = 1) -> Task:
    task = Task(**task.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def retrieve_task(task_id: int, db: Session):
    cache_key = f"task:{task_id}"

    cached_task = cache.get(cache_key)
    if cached_task:
        task = json.loads(cached_task)
        task["create_at"] = datetime.fromisoformat(task["create_at"])
        return task

    task = db.query(Task).filter(Task.task_id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task_data = json.dumps({"title": task.title,
                            "description": task.description,
                            "owner_id": task.owner_id,
                            "create_at": task.create_at.isoformat(),
                            })

    cache_set(cache_key, task_data)

    return {"title": task.title,
            "description": task.description,
            "owner_id": task.owner_id,
            "create_at": task.create_at,
    }


def list_tasks(db: Session):
    # TODO: add redis ( set and update redis databases)
    tasks = db.query(Task).filter(Task.is_active == True).all()
    return tasks


def update_task(task_id: int, task: UpdateTask, owner_id: int, db: Session):
    task_in_db = db.query(Task).filter(task_id == Task.task_id).first()
    if not task:
        return
    task_in_db.title = task.title
    task_in_db.description = task.description
    db.add(task_in_db)
    db.commit()
    return task_in_db


def delete_task(task_id: int, owner_id: int, db: Session):
    task_in_db = db.query(Task).filter(Task.task_id == task_id)
    if not task_in_db.first():
        return {"error": f"cannot find task with id: {task_id}"}
    if not task_in_db.first().owner_id == owner_id:
        return {"error": "only owner can delete task"}
    task_in_db.delete()
    db.commit()
    return {"massage": f"deleted task with id: {task_id}"}
