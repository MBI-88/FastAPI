from fastapi import FastAPI, Response, Path
import uvicorn
from enum import Enum


class UserType(Enum):
    ADMIN: str = "Admin"
    STANDARD: str = "Standar"


app = FastAPI()


@app.get("/")
async def index() -> Response:
    return {"message": "Hola mundo"}


@app.get("/user/{type}/{id}")
async def get_user(id: int, type: str) -> Response:
    return {"type": type, "id": id}


# Uso de Enum para limitar datos solo acepta (Admin , Standar) como string
@app.get("/user-type/{type}")
async def get_limite_string(type: UserType) -> Response:
    return {"type": type}


@app.get("/license-plates/{license}")
async def get_license(license:str = Path(...,min_length=9,max_length=9)) -> Response:
    return {"license":license}


@app.get("/license-plate-regex/{license}")
async def get_license_regex(license:str = Path(...,regex=r"^\w{2}-\d{3}-\w{2}$")) -> Response:
    return {"license-regex":license}


if __name__ == "__main__":
    uvicorn.run("path:app", host="localhost", port=8000, reload=True)
