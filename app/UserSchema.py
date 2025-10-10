# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint, Field
import random

def generate_user_id() -> str:
    # Generate a user ID like BA123456 (BA means Budget Air)
    return f"BA{random.randint(100000, 999999)}"

class User(BaseModel):
    user_id: str = Field(default_factory=generate_user_id)
    username: constr(min_length=3, max_length=18)
    password: constr(min_length=5, max_length=12)
    passport_type: str
    firstname: constr(min_length=2, max_length=50)
    lastname: constr(min_length=2, max_length=50)
    email: EmailStr
    age: conint(gt=18)
    number: constr(min_length=10, max_length=10)
    #0852012545
