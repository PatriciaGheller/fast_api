from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.controllers import auth
from src.database import database
from src.controllers import post


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()
    
    

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)



