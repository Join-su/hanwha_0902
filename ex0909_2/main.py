from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum


app = FastAPI()

class ItemSchema(BaseModel):
    name:str
    price:float
    desc:str | None=None


items_db:dict[int, dict] = {}
id_counter=1


# 생성create
@app.post("/items/", status_code=201)
async def create_item(item:ItemSchema):
    global id_counter
    item_dump=item.model_dump()
    items_db["id"]=id_counter

    items_db[id_counter]=item_dump
    id_counter +=1

    return{
        "msg" : f"{item.name} 추가 완료",
        "all_item" : items_db,
    }



# 조회(전체)read
@app.get("/items/")
async def get_all_items():
    return {"msg":"전체 목록 조회 완료", "data":list(items_db.values())}


# 조회(단일)read
@app.get("/items/{item_id}")
async def get_item(item_id:int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="아이템이 없습니다")

    return {"msg":"단일 조회 완료", "data" : items_db[item_id]}

# 수정update
@app.put("/items/{item_id}")
async def update_item(item_id:int, item:ItemSchema):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="아이템이 없습니다")

    update_data = item.model_dump()
    update_data["id"] = item_id
    items_db[item_id] = update_data

    return {"msg":"수정 완료", "data" : update_data}


#삭제delete
@app.delete("/items/{item_id}")
async def delete_item(item_id:int):

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="아이템이 없습니다")

    delete_item = items_db.pop(item_id)

    return {"msg" : "삭제 완료", "data" :delete_item}