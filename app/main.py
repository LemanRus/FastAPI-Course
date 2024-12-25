from fastapi import FastAPI, Cookie, Response
from fastapi.responses import FileResponse
from random import randint
from models.models import User, Product

app = FastAPI()

sample_user: dict = {"username": "user123", "password": "password123"}
mock_db: list[User] = [User(**sample_user)]
sessions: dict = {}

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3,
                   sample_product_4, sample_product_5]


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


@app.get("/user")
async def get_user(session_token = Cookie()):
    print(session_token)
    user = sessions.get(session_token)
    if user:
        return user.dict()
    return {"message": "Unauthorized"}


@app.get("/show_users")
async def show_users():
    return {"users": mock_db}


@app.post("/user_create")
async def create_user(user: User) -> User:
    mock_db.append(user)
    return user


@app.post("/login")
async def login(user: User, response: Response):
    for person in mock_db:
        if person.username == user.username and person.password == user.password:
            session_token = "".join([chr(randint(32, 120)) for _ in range(0, 32)])
            sessions[session_token] = user
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return {"message": "куки установлены"}
    return {"message": "Invalid username or password"}


@app.get("/product/{product_id}")
async def show_product(product_id: int) -> Product | dict:
    for product in sample_products:
        if product["product_id"] == product_id:
            return Product(**product)
    return {"message": "Product not found"}


@app.get("/products/search")
async def search_product(keyword: str, category: str | None = None,
                         limit: int | None = None) -> list[Product]:
    found = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if product["category"].lower() == category.lower():
                found.append(Product(**product))

    return found[:limit]
