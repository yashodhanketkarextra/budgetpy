from fastapi import FastAPI

from src.routes.root import rootRouter
from src.routes.users import userRouter

app = FastAPI()


app.include_router(rootRouter)
app.include_router(userRouter)
