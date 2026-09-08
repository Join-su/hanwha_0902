from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum # 열거형

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"Hello": "World"}

# http://127.0.0.1:8000/items/123
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# http://127.0.0.1:8000/items/123
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

# http://127.0.0.1:8000/users/me
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

# http://127.0.0.1:8000/users/사용자
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# http://127.0.0.1:8000/models/lenet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


###############################

