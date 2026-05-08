import tracemalloc
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import Base, engine
from src.routes.root import rootRouter
from src.routes.users import userRouter

tracemalloc.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(rootRouter)
app.include_router(userRouter)
