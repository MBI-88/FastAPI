from typing import List
from fastapi import FastAPI, Form, Response, File, UploadFile
import uvicorn

app = FastAPI()


@app.post("/user")
async def create_user(name: str = Form(...), age: int = Form(...)) -> Response:
    return {"name": name, "age": age}


@app.post("/file")
async def upload(file: bytes = File(...)) -> Response:
    return {"file_size": len(file)}


@app.post("/big-file")
async def upload_bigfile(file: UploadFile = File(...)) -> Response:
    return {"big-file": file.filename, "content_type": file.content_type}


@app.post("/list-files")
async def upload_listfile(files: List[UploadFile] = File(...)) -> Response:
    return [{
        "file_name": file.filename, "content_type": file.content_type
    } for file in files]

if __name__ == "__main__":
    uvicorn.run("form_data:app", host="localhost", port=8000, reload=True)
