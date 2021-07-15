from typing import Optional, List, Set
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    results = {"item_id": item_id, **item.dict()}
    if q:
        results.update({"q": q})
    return results


@app.put("/items2/{item_id}")
async def update_item2(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }

    if q:
        results.update({"q": q})
    return results


@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database"
                    "that have a good match",
        alias="item-query",
        min_lenght=3,
        max_length=50
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_items_detail(
    item_id: int = Path(..., title="The ID of the item to get", ge=2, le=5),
    q: Optional[str] = Query(None, alias="item-qeury")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
