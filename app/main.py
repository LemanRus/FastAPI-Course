from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.models import User

app = FastAPI()

my_user: User = User(name="Stephen Hawking", id=1)

@app.get("/")
async def root():
    return FileResponse("./app/index.html")


@app.post("/calculate")
async def calc(num_a: float, num_b: float):
    return {"result": num_a + num_b}


@app.get("/users")
async def show_user():
    return my_user