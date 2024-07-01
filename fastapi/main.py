import os

import sqlalchemy
from fastapi import FastAPI, Request

import sqlalchemy
import databases

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

import bcrypt


DATABASE_URL = os.getenv("")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

metadata = sqlalchemy.MetaData()

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", EmailStr, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/registration", response_class=HTMLResponse)
async def rendering_register(request: Request):
    return templates.TemplateResponse("registration.html", context={"request": request})


@app.post("/registration", response_model=UserOut)
async def registration(user_in: UserIn):
    user_save = create_user(user_in)
    return user_save
