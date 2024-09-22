from fastapi import FastAPI
from routes import route

# App

app = FastAPI()

@app.get('/index')
async def index() -> dict:
    return {"message":"Welcome to FastApi"}

app.include_router(router=route)