from contextlib import asynccontextmanager

from controllers import post
from fastapi import FastAPI
from database import database, metadata, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.post import posts
    
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.connect()
    
    

app = FastAPI(lifespan=lifespan)
app.include_router(post.router)



