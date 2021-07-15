from enum import Enum
from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/models/{model_name}/")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW"}
    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    if model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}/")
async def read_file(file_path: str):
    return {"file_path": file_path}
