from pydantic import BaseModel

class PostOut(BaseModel):
    title: str
    author: str
    published_at: datetime