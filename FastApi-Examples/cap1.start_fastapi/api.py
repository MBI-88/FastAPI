from fastapi import FastAPI

# api

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'message':'Welcome to FastApi'}