from pydantic import BaseModel

class PostOut(BaseModel):
    title: str
    author: str
    date: datetime