from email.policy import HTTP
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn

# Routes

user_router = APIRouter(tags=["User"])
user_database = Database(User)


@user_router.post('/signup')
async def sign_new_user(user: User) -> dict:
    user_exis = await User.find_one(User.email==user.email)
    if user_exis:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with email provided exists")
    await user_database.save(user)
    return {"message": "User successfully registered!"}


@user_router.post('/signin')
async def sign_user_in(user: UserSignIn) -> dict:
    usr_exit = await User.find_one(User.email == user.email)
    if not usr_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with email does not exist")
    if usr_exit.password == user.password:
        return {"message": "User signed in successfully"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid details passed")
