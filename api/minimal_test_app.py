from fastapi import FastAPI

app = FastAPI()

items = {}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/{item_id}")
def add_item(item_id: int, item: dict):
    items[item_id] = item
    return {"item_id": item_id, "item": item}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "item": items.get(item_id)}
