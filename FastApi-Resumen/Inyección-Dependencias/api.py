from fastapi import FastAPI, Response, Depends, Query, HTTPException, status, Header
import uvicorn
from typing import Tuple, Optional


app = FastAPI()


# Estableciendo el paginado dinámico por medio de clases

class Pagination:
    def __init__(self, maximun_limit: int = 100) -> None:
        self.maximun_limit = maximun_limit

    async def __call__(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)) -> Tuple[int, int]:
        capped_limit = min(self.maximun_limit, limit)
        return (skip, capped_limit)

# Instancia de clase paginación


pagination_instance = Pagination(maximun_limit=50)


async def pagination(skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination)) -> Response:
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination)) -> Response:
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/pagination-instance")
async def list_pagination_items(p: Tuple[int, int] = Depends(pagination_instance)) -> Response:
    skip, limit = p
    return {"skip": skip, "limit": limit}


# Use a dependency on a path decorator

def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)


@app.get("/protected-route", dependencies=[Depends(secret_header)])
async def protected_route() -> Response:
    return {"hello": "world"}




if __name__ == '__main__':
    uvicorn.run('api:app', host='localhost', port=8000, reload=True)
