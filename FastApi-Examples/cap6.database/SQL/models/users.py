from pydantic import BaseModel, EmailStr
from models.events import Event
from typing import Optional, List

# Events


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Config:
        schema_extra = {
            "example": {
                "email": 'fastapi@packt.com',
                "password": "strong!!!",
                "events": [],

            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": 'fastapi@packt.com',
                "password": "strong!!!",
                "events": [],

            }
        }