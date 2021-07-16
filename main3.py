from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The Bar fighters",
        "price": 62,
        "tax": 20.2
    },
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    emial: EmailStr
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, 'item': item}
    return results


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude=["tax"]
)
async def read_item_public_data(item_id: str):
    return items[item_id]
