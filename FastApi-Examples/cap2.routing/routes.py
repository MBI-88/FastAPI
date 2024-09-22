from fastapi import APIRouter,Path
from model import ValidData

# Routes

routes = APIRouter()

db_list = []

@routes.get('/getdb')
async def getdb() -> dict:
    return {'message':db_list}

@routes.post('/getdb')
async def postdb(data:ValidData) -> dict:
    db_list.append(data)
    return {'message':'Post succesfull!'}

@routes.get('/getid/{id}')
async def getId(id:int = Path(...,title="The id of the item ")) -> dict:
    for db in db_list:
        if id == db.id:
            return {'message': db} 
    
    return {'message':'Not found'}

@routes.put('/getdb/{id}')
async def putdb(data:ValidData,id:int = Path(...,title="Id of item for updating")) -> dict:
    for db in db_list:
        if db.id == id:
            db.item = data.item
            return {'message':"Update item succesful"}
    return {"message":"Not access"}

@routes.delete('/getdb/{id}')
async def deletedb(id:int) -> dict:
    for index in range(len(db_list)):
        db = db_list[index]
        if db.id == id:
            db_list.pop(index)
            return {'message':'Item delelted successful','db-length':len(db_list)}
    return {'message':'Not access'}

@routes.delete('/dbclear')
async def deleteAll() -> dict:
    db_list.clear()
    if len(db_list) == 0:
        return {'message':'Succeful action'}
    return {'message':'Not access'}