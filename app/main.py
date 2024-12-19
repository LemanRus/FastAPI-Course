from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.models import User, UserCreate, Product

app = FastAPI()
mock_db: list[UserCreate] = []

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

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

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


@app.get("/product/{product_id}")
async def show_product(product_id: int) -> Product | dict:
    for product in sample_products:
        if product["product_id"] == product_id:
            return Product(**product)
    return {"message": "Product not found"}

@app.get("/products/search")
async def search_product(keyword: str, category: str | None = None, limit: int | None = None) -> list[Product]:
    found = []
    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if product["category"].lower() == category.lower():
                found.append(Product(**product))

    return found[:limit]