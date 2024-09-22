from fastapi import FastAPI, Response, status, HTTPException, Body
from fastapi.responses import (HTMLResponse, PlainTextResponse, 
                               RedirectResponse, FileResponse)
import os
import uvicorn
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    nb_views: int


class PublicPost(BaseModel):
    title: str


posts = {
    1: Post(title="Hello", nb_views=100)
}

app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> Response:
    return {"message": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> None:
    posts.pop(id, None)
    return None


@app.get("/posts/{id}", response_model=PublicPost)
async def get_post(id: int) -> Response:
    return posts[id]


@app.get("/")
async def custom_header(response: Response) -> Response:
    response.headers["Custom-Header"] = "Custom-Header-Value"
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {"hello": "world"}


@app.post("/password")
async def check_password(password: str = Body(...), password_confirm: str = Body(...)) -> Response:
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match"
        )

    return {"message": "Password match"}


@app.get("/html", response_class=HTMLResponse)
async def get_html() -> HTMLResponse:
    return """
    <html>
<head>
<title>Hello world!</title>
</head>
<body>
<h1>Hello world!</h1>
</body>
</html>
"""


@app.get("/text", response_class=PlainTextResponse)
async def get_plaintext() -> PlainTextResponse:
    return "Hello world!"


@app.get("/redirect")
async def redirection() -> RedirectResponse:
    return RedirectResponse("/new-url",
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


@app.get("/cat")
async def get_cat() -> FileResponse:
    root_dir = os.path.dirname(os.path.dirname(__file__))
    picture_path = os.path.join(root_dir,"Resumen-Endpoint","cat.jpg")
    print(root_dir)
    return FileResponse(picture_path)


@app.get("/xml")
async def get_xml() -> Response:
    content = """
    <?xml version="1.0" encoding="UTF-8"?>
    <Hello>World</Hello>
    """
    return Response(content=content,media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run('response:app', host='localhost', port=8000, reload=True)
