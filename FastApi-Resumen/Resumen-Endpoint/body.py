from fastapi import FastAPI, Body, Response
import uvicorn
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: str

class Company(BaseModel):
    name:str
    total_workers:int


app = FastAPI()


@app.post("/user")
async def create_user(name: str = Body(...), age: int = Body(...)) -> Response:
    return {"name": name, "age": age}


@app.post("/user-pydantic")
async def create_user_pydantic(user: User) -> Response:
    return {"user": user}

@app.post("/multiples-objects")
async def create_multiples_objects(user:User,company:Company) -> Response:
    return {"user":user,"company":company}



if __name__ == "__main__":
    uvicorn.run("body:app", host="localhost", port=8000, reload=True)
