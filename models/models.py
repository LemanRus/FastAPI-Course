from idlelib.query import Query

from pydantic import BaseModel, PositiveInt, Field, EmailStr
from decimal import Decimal

from unicodedata import decimal


class User(BaseModel):
    name: str
    age: int
    is_adult: bool = False


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = Field(default=None, lt=130)
    is_subscribed: bool = False


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: Decimal = Field(decimal_places=2)
