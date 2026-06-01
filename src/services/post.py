from databases.interfaces import Record
from fastapi import HTTPException, status
from src.models.post import posts
from src.schemas.post import PostIn, PostUpdateIn
from src.database import database
from sqlalchemy import select, update, delete


class PostService:
    async def read_all(self, published: bool, limit: int, skip: int) -> list[Record]:
        query = select(posts).where(posts.c.published == published).limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, post: PostIn) -> int:
        command = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=post.published_at,
            published=post.published,
        )
        return await database.execute(command)

    async def read(self, id: int) -> Record:
        return await self._get_by_id(id)

    async def update(self, id: int, post: PostUpdateIn) -> Record:
        total = await self.count(id)
        if not total:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        data = post.model_dump(exclude_unset=True)
        command = update(posts).where(posts.c.id == id).values(**data)
        await database.execute(command)

        return await self._get_by_id(id)

    async def delete(self, id: int) -> None:
        total = await self.count(id)
        if not total:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        command = delete(posts).where(posts.c.id == id)
        await database.execute(command)

    async def count(self, id: int) -> int:
        query = select(posts.c.id).where(posts.c.id == id)
        result = await database.fetch_one(query)
        return 1 if result else 0

    async def _get_by_id(self, id: int) -> Record:
        query = select(posts).where(posts.c.id == id)
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return result
