from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timezone,timedelta

from app.db.database import db


from config import settings
SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_EXPIRY=settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRY=settings.REFRESH_TOKEN_EXPIRE_DAYS

password_hash=PasswordHash((
    Argon2Hasher(),
    ))

def hash_password(password:str)->bool:
    return password_hash.hash(password)

def verify_password(password:str,hashed_password:str):
    result= password_hash.verify(password,hashed_password)

    if not result:
        raise HTTPException(
            status_code=403,
            detail='Wrong username or password!'
        )
    return result
#JWT Tokens

def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    to_encode.update({'exp':expire,'type':'access'})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRY)
    to_encode.update({'exp':expire,'type':'refresh'})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

#Verify Tokens

def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('type')=='access':
            return payload
        else: raise InvalidTokenError
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Invalid Token'
        )
def verify_refresh_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('type')=='refresh':
            return payload
        else: raise InvalidTokenError
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Invalid Token'
        )

#User and admin verification

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='user/login')
#bearer tokenxyz -> removed bearer -> tokenxyz

async def get_current_user(token:str=Depends(oauth2_scheme)):
    access_token=verify_access_token(token)
    user_id=access_token.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail='Authentication error'
        )
    user=await db.users.find_one({'_id':user_id})
    if not user:
        raise HTTPException(
            status_code=401,
            detail='Authentication error'
        )
    return user

def get_current_admin(user:dict=Depends(get_current_user)):
    if user.get('role')!='admin':
        raise HTTPException(
            status_code=403,
            detail='Forbidden'
        )
    return user

