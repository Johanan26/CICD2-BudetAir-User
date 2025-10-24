# app/schemas.py
from typing import Annotated, Optional, List
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, ConfigDict, StringConstraints
from pydantic import BaseModel, EmailStr, constr, conint, Field
import random

def generate_user_id() -> str:
    # Generate a user ID like BA123456 (BA means Budget Air)
    return f"BA{random.randint(100000, 999999)}"

#-----------Reusable type aliases-------------
firstname= Annotated[str,StringConstraints(min_length=2, max_length=50)]
lastname= Annotated[str,StringConstraints(min_length=2, max_length=50)]
username= Annotated[str,StringConstraints(min_length=3, max_length=18)]
user_id=Annotated[str, Field(default_factory=generate_user_id)]
password=Annotated[str,StringConstraints(min_length=5, max_length=12)]
email = Annotated[EmailStr, StringConstraints(max_length=100)]
age=Annotated[int, Ge(0), Le(150)]
number=Annotated[int, Ge(10), Le(10)]

#class User(BaseModel):
   # user_id: str = Field(default_factory=generate_user_id)
   # username: constr(min_length=3, max_length=18)
    #password: constr(min_length=5, max_length=12)
    #passport_type: str
    #firstname: constr(min_length=2, max_length=50)
    #lastname: constr(min_length=2, max_length=50)
    #email: EmailStr
   # age: conint(gt=18)
   # number: constr(min_length=10, max_length=10)
    #0852012545 
#--------Users----------
class User(BaseModel):
    firstname: firstname
    lastname: lastname
    username: username
    user_id: user_id
    password: password
    email: email
    age: age
    number: number
