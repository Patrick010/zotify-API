from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI()

items: Dict[int, Dict[str, Any]] = {}


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.post("/items/{item_id}")
def add_item(item_id: int, item: Dict[str, Any]) -> Dict[str, Any]:
    items[item_id] = item
    return {"item_id": item_id, "item": item}


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Dict[str, Any]:
    return {"item_id": item_id, "item": items.get(item_id)}
