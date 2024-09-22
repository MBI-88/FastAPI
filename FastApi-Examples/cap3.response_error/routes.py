from model import TodoItems
from fastapi import APIRouter,status,HTTPException,Path

# Routes

route = APIRouter()

database = [
    {"id":1,"item":"Item 1"},{"id":2,"item":"Item 2"},{"id":3,"item":"Item 3"},{"id":4,"item":"Item 4"}
]

@route.get('/getdata', response_model=TodoItems,status_code=200)
async def getData() -> dict:
    return {"items": database}

@route.get('/getitem/{itemId}',status_code=200)
async def getItem(itemId:int = Path(...,title="Item id")) -> dict:
    for db_item in database:
        if db_item['id'] == itemId:
            return {"message":db_item}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not exists")