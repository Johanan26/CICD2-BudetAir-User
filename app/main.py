# app/main.py
from fastapi import FastAPI, HTTPException, status
from .UserSchema import User, generate_user_id #import the generate function from the schema

app = FastAPI()
users: list[User] = []

#Get all the users
@app.get("/api/users")
def get_users():
    return users

#Gets all users using their id
@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#Creates new users and shows an error if user already exists
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if not user.user_id:# Only generate an ID if not already provided
     user.user_id = generate_user_id() #call the function to generate the user id
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

#Updates users and shows an error if user already exists
@app.put("/api/users/{username}")
def update_user(username: str, updated_user: User):
    for i, u in enumerate(users):
        if u.username == username:
            users[i] = updated_user
            return updated_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

#Deletes users and shows an error if user id is not found
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str): #changing from int to string as our user id is now a string not an int, causing test fails
    for u in users:
        if u.user_id == user_id:
            users.remove(u)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="user_id not found"
    )
