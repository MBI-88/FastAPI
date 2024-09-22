from fastapi import FastAPI, Response


app = FastAPI()


@app.get("/")
async def hello_world() -> Response:
    return {"hello": "world"}


@app.on_event("startup")
async def startup() -> None:
    print("Startup")


@app.on_event("shutdown")
async def shutdown() -> None:
    print("Shutdown")
