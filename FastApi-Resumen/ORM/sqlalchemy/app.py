from typing import List, Tuple, cast, Mapping
from databases import Database
from fastapi import Depends, FastAPI, HTTPException, Query, status
from database import get_database, sqlalchemy_engine
from models import (
    metadata, posts, PostDB, PostCreate, PostPartialUpdate, comments,
    CommentCreate, CommentDB
)


app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown() -> None:
    await get_database().disconnect()


async def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_post_or_404(id: int, database: Database = Depends(get_database)) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
    pagination: Tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database)
) -> List[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    results = [PostDB(**row) for row in rows]

    return results


@app.get("/post/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, database: Database = Depends(get_database)) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)

    post_db = await get_post_or_404(post_id, database)
    return post_db


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(post_update: PostPartialUpdate, post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)) -> PostDB:
    update_query = (
        post.update().where(posts.c.id == post.id).values(
            post_update.dict(exclude_unset=True))

    )
    await database.execute(update_query)
    post_db = await get_post_or_404(post.id, database)
    return post_db


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostDB = Depends(get_post_or_404), database: Database = Depends(get_database)) -> None:
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)


@app.post("/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate, database: Database = Depends(get_database)
) -> CommentDB:
    select_post_query = posts.select().where(posts.c.id == comment.post_id)
    post = await database.fetch_one(select_post_query)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post {comment.post_id} does not exist",
        )

    insert_query = comments.insert().values(comment.dict())
    comment_id = await database.execute(insert_query)

    select_query = comments.select().where(comments.c.id == comment_id)
    raw_comment = cast(Mapping, await database.fetch_one(select_query))

    return CommentDB(**raw_comment)
