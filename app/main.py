import jwt
from datetime import datetime, timedelta
from random import randint

from fastapi import FastAPI, Cookie, Response, Header, Request, HTTPException, Depends, status
from fastapi.security import  HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.responses import FileResponse

from models.models import User, Product

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
EXP_TIME = timedelta(minutes=5)

mock_db: list[User] = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]
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


# симуляционный пример
def get_user_from_db(username: str):
    for user in mock_db:
        if user.username == username:
            return user
    return None


def authenticate_user(credentials: HTTPBasicCredentials = Depends(oauth2_scheme)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return True


def create_jwt_token(data: dict):
    data.update({"exp": datetime.now() + EXP_TIME})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


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
async def login(user_in: User):
    if authenticate_user(user_in):
        return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
    return {"error": "Invalid credentials"}


@app.get("/login")
async def login(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome"}


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


@app.get("/headers")
async def get_geaders(request: Request):
    if (user_agent := request.headers["user-agent"]) and (accept_language := request.headers["accept-language"]):
        return {
            "User-Agent": user_agent,
            "Accept-Language": accept_language
        }
    raise HTTPException(status_code=400, detail="Required Headers Error")


@app.get("/protected_resource/")
def get_protected_resource(verified_user: dict = Depends(verify_jwt_token)):
    if verified_user:
        return {'message': 'Access to the protected resource is allowed'}
