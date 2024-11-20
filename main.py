from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/calculate")
async def calc(num_a: float, num_b: float):
    return {"result": num_a + num_b}