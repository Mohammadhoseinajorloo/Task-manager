from backend.apis.base import api_router
from backend.apps.base import app_router
from backend.core.config import settings
from backend.db.base import Base
from backend.db.session import engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_table():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")


def start_appliction():
    app = FastAPI()
    create_table()
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_appliction()
