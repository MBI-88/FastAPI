from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.events import event_router
from database.connection import conn
import uvicorn

# Api

app = FastAPI()

app.include_router(user_router,prefix='/user')
app.include_router(event_router,prefix='/event')

@app.on_event("startup")
def on_startup() -> None:
    conn()

@app.get('/')
async def index() -> RedirectResponse:
    return RedirectResponse(url='/event')

if __name__ == "__main__":
    uvicorn.run("manage:app", host="localhost",port=8080,reload=True)