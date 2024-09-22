from fastapi import FastAPI, Response, Request
import uvicorn


app = FastAPI()


@app.get("/")
async def get_request(request: Request) -> Response:
    return {"path": request.url.path}


if __name__ == "__main__":
    uvicorn.run('request_object:app', host="localhost", port=8000, reload=True)
