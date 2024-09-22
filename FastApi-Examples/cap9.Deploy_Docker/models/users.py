from pydantic import BaseModel, EmailStr
from beanie import Document

# Events


class User(Document):
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": 'fastapi@packt.com',
                "password": "strong!!!",
            }
        }


class TokenResponse(BaseModel):
    access_token:str
    token_type:str
