from apis.v1 import route_task
from apis.v1 import route_login
from fastapi import APIRouter

app_router = APIRouter()

app_router.include_router(
    route_task.router, prefix="", tags=[""], include_in_schema=False
)

app_router.include_router(
    route_login.router, prefix="/auth", tags=[""], include_in_schema=False
)