from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.models import User

app = FastAPI()


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