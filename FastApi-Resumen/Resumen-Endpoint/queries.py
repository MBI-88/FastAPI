from fastapi import FastAPI, Response, Query
import uvicorn


app = FastAPI()


@app.get("/users")
async def get_users(page: int = 1, size: int = 10) -> Response:
    return {"page": page, "size": size}


@app.get("/users-queries")
async def get_queries(page: int = Query(1, gt=0), size: int = Query(10, le=100)) -> Response:
    return {"page": page, "size": size}


if __name__ == "__main__":
    uvicorn.run("queries:app", host="localhost", port=8000, reload=True)
