from pydantic import BaseModel, PositiveInt, Field, EmailStr
from decimal import Decimal


class User(BaseModel):
    name: str
    username: str
    password: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False
    is_adult: bool = False


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: Decimal = Field(decimal_places=2)
