from pydantic import BaseModel
from typing import Optional,List
from fastapi import Form

# Models

class Todo(BaseModel):
    id:Optional[int]
    item:str
    
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "item":"New Item"
            }
        }
    
    @classmethod
    def as_form(cls,item:str = Form(...)) -> object:
        return cls(item=item)

class TodoItem(BaseModel):
    item:str
    
    class Config:
        scheam_extra = {
            "example":{
                "item":"Item created"
            }
        }

class TodoItems(BaseModel):
    todo: List[TodoItem]
    
    class Config:
        schema_extra = {
            "example": {
                "todo": [
                    {
                        "item":"First item"
                    },
                    {
                        "item":"Second item"
                    }
                ]
            }
        }