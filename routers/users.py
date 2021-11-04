from fastapi import APIRouter, Depends, HTTPException
from modules import auth, database
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    email: str
    password: str

class UserToken(BaseModel):
    uuid: str
    jwt: str

@router.post("/api/user/add", response_model=UserToken, tags=["users"])
async def add_user(user: User):
    identifier = auth.generate_uuid(user.email)
    if not database.user_exists(identifier):
        hashed_password = auth.generate_hash(user.password)
        database.add_user(identifier, hashed_password)
        return {"uuid": identifier, "jwt": auth.generate_jwt(identifier)}
    raise HTTPException(status_code=403)

@router.post("/api/user/auth", response_model=UserToken, tags=["users"])
async def authenticate_user(user: User):
    identifier = auth.generate_uuid(user.email)
    if database.user_exists(identifier):
        if auth.check_password(user.password, database.user_hash(identifier)):
            return {"uuid": identifier, "jwt": auth.generate_jwt(identifier)}
    raise HTTPException(status_code=401)

@router.get("/api/user/tasks", tags=["users"])
async def view_user_tasks(identifier: str = Depends(auth.header_to_identifier)):
    if identifier:
        return database.list_task(identifier)
    raise HTTPException(status_code=401)
