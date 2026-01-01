# app/schemas.py
from typing import Annotated
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, StringConstraints
from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4

def generate_user_id() -> str:
    # Generate a user ID like BA6afedb67-d26c-46a0-bf47-528cdbfaab9a (BA means Budget Air)
    # NOTE: the reason for UUID instead of something like generating random numbers is due to UUID almost never being able to be the same.
    # even if we create a billion uuids per second for 100 years there is only a 50% chance its the same(doubt we will generate that many users though)
    return f"BA{uuid4()}"

#-----------Reusable type aliases-------------
firstname= Annotated[str,StringConstraints(min_length=2, max_length=50)]
lastname= Annotated[str,StringConstraints(min_length=2, max_length=50)]
username= Annotated[str,StringConstraints(min_length=3, max_length=18)]
user_id=Annotated[str, StringConstraints(min_length=5, max_length=100)]
password=Annotated[str,StringConstraints(min_length=5, max_length=12)]
email = Annotated[EmailStr, StringConstraints(max_length=100)]
age=Annotated[int, Ge(0), Le(150)]
number=Annotated[str, StringConstraints(min_length=10, max_length=10)]

#--------Users----------

class User(BaseModel):
    firstname: firstname
    lastname: lastname
    username: username
    password: password
    email: email
    age: age
    number: number

class UserPublic(BaseModel):
    user_id: str
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    age: int
    number: str

    class Config:
        orm_mode = True
