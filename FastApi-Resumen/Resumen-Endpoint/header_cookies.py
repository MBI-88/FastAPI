from fastapi import Cookie, FastAPI,Response,Header
import uvicorn
from typing import Optional


app = FastAPI()


@app.get("/")
async def get_header(hello:str = Header(...)) -> Response:
    return {"hello":hello}

@app.get("/header")
async def get_header_query(user_agent:str = Header(...)) -> Response:
    return {"user_agent":user_agent}

@app.get("/cookie")
async def get_cookie(hello: Optional[str] = Cookie(None)) -> Response:
    return {"hello": hello}


if __name__ == "__main__":
    uvicorn.run("header_cookies:app",host="localhost",port=8000,reload=True)
    