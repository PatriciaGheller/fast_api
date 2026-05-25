from datetime import UTC, datetime
from typing import Annotated

from fastapi import Cookie, Header, Response, status
from main import app
from schemas.post import PostIn
from views.post import PostOut

fake_db = [
    {"title": f"Criando uma aplicação com FastAPI", "date": datetime.now(UTC),"published": True },
    {"title": f"Criando uma aplicação com Flask", "date": datetime.now(UTC),"published": True}, 
    {"title": f"Criando uma aplicação com Django", "date": datetime.now(UTC),"published": True}, 
    {"title": f"Criando uma aplicação com Starlett", "date": datetime.now(UTC),"published": False },
]


@app.post('/post/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    fake_db.append(post.model_dump())
    return post


@app.get("/posts", response_model=list[PostOut])
def read_posts(  
    response: Response, 
    published: bool, 
    limit: int, 
    skip: int = 0, 
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    
    response.set_cookie(key="user", value="patricia.gheller.1985@gmail.com")
    print(f"Cookie: {ads_id}")
    print(f"User-agent: {user_agent}")
    return [post for post in fake_db[skip : skip + limit] if post["published"] is published]

@app.get("/posts/{framework}", response_model=PostOut)
def read_framework_posts(framework: str):
    return {
        "posts": [
            {"title": f"Criando uma aplicação com {framework}", "date": datetime.now(UTC)}, 
            {"title": f"Criando uma aplicação com {framework}", "date": datetime.now(UTC)}
        ]
    }