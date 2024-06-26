from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import db
from .router import router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await db.create_tables()
#     yield

app = FastAPI(
    title="VK_bot_farm",
    # lifespan=lifespan
)

app.include_router(router=router)
