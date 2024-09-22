from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
import uvicorn

# Api

app = FastAPI()
settings = Settings()
app.include_router(user_router,prefix='/user')
app.include_router(event_router,prefix='/event')

@app.on_event("startup")
async def initDB() -> None:
    await settings.initialize_database()

@app.get('/')
async def index() -> RedirectResponse:
    return RedirectResponse(url='/event')

if __name__ == "__main__":
    uvicorn.run("manage:app", host="localhost",port=8080,reload=True)