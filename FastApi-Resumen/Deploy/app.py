from typing import List, Tuple
from fastapi import Depends, FastAPI, Query, status
from tortoise.contrib.fastapi import register_tortoise
from settings import Settings

settings = Settings()
app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.on_event("startup")
async def startup():
    if settings.debug:
        print(settings)


TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
