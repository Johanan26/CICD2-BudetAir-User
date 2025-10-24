# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from .Userdb import engine, SessionLocal
from .Usermodels import Base, UserDB
from .UserSchema import User, generate_user_id #import the generate function from the schema

app = FastAPI()
users: list[User] = []

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commit_or_rollback(db: Session, error_msg: str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=error_msg)


#Get all the users
@app.get("/api/users", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    user = db.query(UserDB).all()
    return users

#Gets all users using their id
@app.get("/api/users/{user_id}",response_model=User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

#Creates new users and shows an error if user already exists
@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
def add_user(user: User, db: Session = Depends(get_db)):
    if not user.user_id:# Only generate an ID if not already provided
     user.user_id = generate_user_id() #call the function to generate the user id
     #Check for dupli
     existing_user =(
        db.query(UserDB).filter(UserDB.user_id == user.user_id).first()
     )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")

    new_user = UserDB(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        password=user.password,
        email=user.email,
        age=user.age,
        number=user.number,
        user_id=user.user_id,
    )

    db.add(new_user)
    commit_or_rollback(db, "Could not create user due to database conflict")
    db.refresh(new_user)
    return new_user

#Updates users and shows an error if user already exists
@app.put("/api/users/{username}", response_model=User)
def update_user(username: str, updated_user: User, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    user.firstname=updated_user.firstname,
    user.lastname=updated_user.lastname,
    user.username=updated_user.username,
    user.password=updated_user.password,
    user.email=updated_user.email,
    user.age=updated_user.age,
    user.number=updated_user.number
    user.user_id=updated_user.user_id

    commit_or_rollback(db, "Could not create user due to database conflict")
    db.refresh(user)
    return new_user

# DELETE a user (triggers ORM cascade -> deletes their projects too)
@app.delete("/api/users/{username}", status_code=204)
def delete_user(username: str, db: Session = Depends(get_db)) -> Response:
    user = db.get(UserDB, username).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user) # <-- triggers cascade="all, delete-orphan" on projects
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
