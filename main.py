from datetime import UTC, datetime
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

fake_db = [
    {"title": f"Criando uma aplicação com FastAPI", "date": datetime.now(UTC),"published": True },
    {"title": f"Criando uma aplicação com Flask", "date": datetime.now(UTC),"published": True}, 
    {"title": f"Criando uma aplicação com Django", "date": datetime.now(UTC),"published": True}, 
    {"title": f"Criando uma aplicação com Starlett", "date": datetime.now(UTC),"published": False },
]

class Post(BaseModel):
    title: str
    date: datetime = datetime.now(UTC)
    published: bool = False
    


@app.post('/post/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    fake_db.append(post.model_dump())
    return post

@app.get("/posts")
def read_posts(  published: bool, limit: int, skip: int = 0):
    return [post for post in fake_db[skip : skip + limit] if post["published"] is published]


@app.get("/posts/{framework}")
def read_framework_posts(framework: str):
    return {
        "posts": [
            {"title": f"Criando uma aplicação com {framework}", "date": datetime.now(UTC)}, 
            {"title": f"Criando uma aplicação com {framework}", "date": datetime.now(UTC)}
        ]
    }


