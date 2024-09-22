from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError, Field, root_validator, validator


class Gender(str, Enum):  # Se usa Enum para crear un set de valores
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NON_BINARY = 'NON_BINARY'


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    gender: Gender
    age: Optional[int] = Field(None, ge=0, le=120)
    birthdate: date
    interests: List[str]
    address: Address

    @validator("birthdate")
    def valid_birthdate(cls, v: date) -> date:
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v

    def name_dict(self) -> dict:
        return self.dict(include={"first_name", "last_name"})


# Uso de datos propiedades opcionales
class UserProfile(BaseModel):
    nickname: str
    location: Optional[str] = None
    subscribed_newsletter: bool = True


# Uso de valores dinámicos

def list_factory() -> list[str]:
    return ["a", "b", "c"]


class Model(BaseModel):
    l: List[str] = Field(default_factory=list_factory)
    d: datetime = Field(default_factory=datetime.now)
    l2: List[str] = Field(default_factory=list)


# Validando emails

class User(BaseModel):
    email: EmailStr
    website: HttpUrl


# Patron de diseño

class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f'{self.content[:140]}...'


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @root_validator()
    def password_match(cls, values: dict[str, str]) -> dict[str, str]:
        password = values.get('password')
        password_confirmation = values.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError("Password don't match")

        return values


# Aplicando validación antes del parsedo

class Model(BaseModel):
    values: List[int]

    @validator('values', pre=True)
    def split_string_values(cls, v) -> list:
        if isinstance(v, str):
            return v.split(",")
        return v
