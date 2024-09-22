from fastapi import FastAPI
from routes import routes

# Api

app = FastAPI()

@app.get('/')
async def index() -> dict:
    return {'message':'Welcome to FastApi'}




# Routing
app.include_router(router=routes)