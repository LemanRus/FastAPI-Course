from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.models import User, UserCreate

app = FastAPI()
mock_db: list[UserCreate] = []

@app.get("/")
async def root():
    return FileResponse("./app/index.html")


@app.post("/calculate")
async def calc(num_a: float, num_b: float):
    return {"result": num_a + num_b}


@app.post("/user")
async def check_adult(user: User) -> User:
    if user.age >= 18:
        user.is_adult = True
    return user


@app.get("/show_users")
async def show_users():
    return {"users": mock_db}


@app.post("/user_create")
async def create_user(user: UserCreate) -> UserCreate:
    mock_db.append(user)
    return user
