from datetime import date
from enum import Enum
from typing import List
from pydantic import BaseModel
import pytest


class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NON_BINARY = 'NON_BINARY'


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: List[str]
    address: Address


# Usando fixtures

@pytest.fixture
def address() -> Address:
    return Address(
        street_address='12 Squirell Street',
        postal_code="424242",
        city="Woodtown",
        country="US"
    )


@pytest.fixture
def person(addrees: Address) -> Person:
    return Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",
        interests=["travel", "sports"],
        address=address,
    )


def test_address_country(address:Address) -> None:
    assert address.country == 'US'

def test_person_first(person:Person) -> None:
    assert person.first_name == "John"

def test_person_address(person:Person) -> None:
    assert person.address.city == "Woodtwon"