from backend.db.repository.tasks import create_new_task
from backend.schemas.tasks import CreateTask
from sqlalchemy.orm import Session
from backend.tests.utils.user import create_random_user


def create_random_task(db: Session):
    task = CreateTask(title="first_task", description="description")
    user = create_random_user(db=db)
    task = create_new_task(task=task, db=db, owner_id=user.id)
    return task
