from unicodedata import name
from pydantic import BaseModel 

# Validation model
"""
class Item(BaseModel):
    name:str
    stauts:str

class ValidData(BaseModel):
    id:int
    item:Item
    
"""
class ValidData(BaseModel):
    id:int
    item:str
    
    class Config:
        Schema_extra = {
            "Example":{
                "id":1,
                "item":"Item name"
            }
        }