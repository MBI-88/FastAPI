from urllib import request
from fastapi import APIRouter, Path, status, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItems

# Routes

route = APIRouter()
template = Jinja2Templates(directory='templates/')

database = []


@route.get('/getdata', response_model=TodoItems)
async def getData(request: Request) -> dict:
    return template.TemplateResponse('data.html', status_code=200, context={'request': request, 'todos': database})


@route.post('/getdata')
async def postData(request: Request, todo: Todo = Depends(Todo.as_form)) -> dict:
    todo.id = len(database) + 1
    database.append(todo)
    return template.TemplateResponse("data.html", status_code=201, context={"request": request, "todos": database})


@route.get('/getitem/{pk}')
async def getItem(request: Request, pk: int = Path(..., title="Id of item")) -> dict:
    for db in database:
        if db.id == pk:
            return template.TemplateResponse('data.html', status_code=status.HTTP_200_OK, context={
                "request": request, "todo": db
            })
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found")
