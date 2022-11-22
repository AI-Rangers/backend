from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# from fastapi import FastAPI 
# app = FastAPI(
#     title="FastAPI - Hello World",
#     description="This is the Hello World of FastAPI.",
#     version="1.0.0",
# ) 
# @app.get("/")
# def hello_world():
#     return {"Hello": "World"}