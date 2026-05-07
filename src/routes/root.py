from fastapi import APIRouter

from src.models.add_item import AddItem

rootRouter = APIRouter()


@rootRouter.get("/")
def read_root():
    return {"Hello": "World"}


@rootRouter.post("/add")
def add_root(item: AddItem):
    return {"result": item.add()}
