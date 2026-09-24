from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError



from app.db.database import db
from app.schemas.users import UserCreate,UserLogin,UserResponse,UserUpdate,ChangeUsername,ChangePassword,ChangeEmail,Token,RefreshToken,AccessToken
from app.core.security import hash_password,verify_password,create_access_token,create_refresh_token,verify_access_token,verify_refresh_token,get_current_admin,get_current_user



router=APIRouter(prefix='/users',tags=['users'])

@router.get('/mongo_rules')
async def enforce_rules():
    result1=await db.users.create_index('email',unique=True)
    result2=await db.users.create_index('username',unique=True)

    return{
        'email':result1,
        'username':result2
    }

@router.post('/refresh',response_model=AccessToken)
def renew_access_token(refresh_token:RefreshToken):
        payload=verify_refresh_token(refresh_token.refresh_token)
        access_token=create_access_token({'sub':payload.get('sub')})
        return{
             'access_token':access_token,
             'token_type':'bearer'
        }

@router.post('/signup',response_model=UserResponse)
async def user_signup(user_input:UserCreate):
    user= user_input.model_dump(exclude_unset=True)
    user['hashed_password']=hash_password(user.pop('password'))
    try:
        result=await db.users.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail='Email or Username already exists'
        )
    #_id->id and objid->str handled by pydantic
    user['_id']=result.inserted_id 
    return user

@router.post('/login',response_model=Token)
async def user_login(user_input:OAuth2PasswordRequestForm=Depends()):

    user=await db.users.find_one({
        '$or':[{'username':user_input.username},
               {'email':user_input.username}]
    })

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Wrong username or password'
        )
    pw_verify=verify_password(user_input.password,user['hashed_password'])

    access_token=create_access_token({'sub':str(user['_id'])})
    refresh_token=create_refresh_token({'sub':str(user['_id'])})

    return{
        'access_token':access_token,
        'refresh_token':refresh_token,
        'token_type':'bearer'
    }

@router.patch('/',response_model=UserResponse)
async def user_edit(user_input:UserUpdate,user:dict=Depends(get_current_user)):
    modified_user=user_input.model_dump(exclude_unset=True)
    query={'_id':user['_id']}
    result=await db.users.find_one_and_update(
         query,
         {'$set':modified_user},
         return_document=ReturnDocument.AFTER
    )
    if not result:
         raise HTTPException(
              status_code=404,
              detail='User not found'
         )
    return result
     



    



