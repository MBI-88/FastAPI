from pydantic import BaseModel
from typing import List

# Models


class TodoItem(BaseModel):
    item: str
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "item": "Read the next chapter of book"
            }
        }


class TodoItems(BaseModel):
    items: List[TodoItem]

    class Config:
        shema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "item": "Example 1"
                     },
                    {
                        "id": 2,
                        "item": "Example 2"
                    },
                ]
            }
        }
