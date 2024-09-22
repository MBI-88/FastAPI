from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
import uvicorn

# Register origins

origins = ["*"]


# Api

app = FastAPI()
settings = Settings()
app.include_router(user_router,prefix='/user')
app.include_router(event_router,prefix='/event') 
app.add_middleware(
    CORSMiddleware,allow_origins=origins,allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"]
)

@app.on_event("startup")
async def initDB() -> None:
    await settings.initialize_database()

@app.get('/')
async def index() -> RedirectResponse:
    return RedirectResponse(url='/event')

if __name__ == "__main__":
    uvicorn.run("manage:app", host="localhost",port=8080,reload=True)