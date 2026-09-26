from pydantic import BaseModel,Field,EmailStr,ConfigDict,field_validator,BeforeValidator
from datetime import date,datetime
import re
from enum import Enum
from typing import Annotated
from pydantic.functional_serializers import PlainSerializer
from bson import ObjectId
from app.schemas.types.custom import PyObjectId as PyObjectID

'''def validate_object_id(value:str|ObjectId)->ObjectId:

    if isinstance(value, ObjectId):
        return value

    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")

    return ObjectId(value)'''




'''PyObjectID=Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(str,return_type=str)
    ]'''

Username=Annotated[
    str,Field(min_length=3,max_length=50)
]

class Sex(str,Enum):
    MALE='male'
    FEMALE='female'
    OTHERS='others'


class UserCreate(BaseModel):
    username:Username
    name:str=Field(min_length=2,max_length=128)
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
    dob:datetime
    sex:Sex

    model_config=ConfigDict(extra='forbid')

    @field_validator('username',mode='before')
    @classmethod
    def validate_username(cls,value):
        if not isinstance(value, str):
            raise ValueError("Username must be a string")
        if not re.fullmatch(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*", value):
            raise ValueError("Username contains invalid characters")
        return value.lower()

    @field_validator('password',mode='after')
    @classmethod
    def validate_password(cls,value):
        if not value.strip():
            raise ValueError('Password can not be blank')
        if value!=value.strip():
            raise ValueError('Password can not start or end with blank spaces')
        return value

class UserLogin(BaseModel):
    identifier:str
    password:str


class UserResponse(BaseModel):
    id:PyObjectID=Field(alias='_id')
    email:EmailStr
    username:str
    name:str
    dob:date
    sex:Sex
    created_at:datetime
    updated_at:datetime

class UserUpdate(BaseModel):
    #username:Username|None=Field(default=None)
    name:str|None=Field(default=None,min_length=2,max_length=128)
    #email:EmailStr|None=None
    #password:str|None=Field(default=None,min_length=6,max_length=128)
    dob:date|None=None
    sex:Sex|None=None

    model_config=ConfigDict(extra='forbid')

class ChangeUsername(BaseModel):
    new_username:Username
    @field_validator('new_username',mode='before')
    @classmethod
    def validate_username(cls,value):
        if not isinstance(value, str):
            raise ValueError("Username must be a string")
        if not re.fullmatch(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*", value):
            raise ValueError("Username contains invalid characters")
        return value.lower()


class ChangeEmail(BaseModel):
    new_email:EmailStr

class ChangePassword(BaseModel):
    old_password:str
    new_password:str=Field(min_length=6,max_length=128)

    @field_validator('new_password',mode='after')
    @classmethod
    def validate_password(cls,value):
        if not value.strip():
            raise ValueError('Password can not be blank')
        if value!=value.strip():
            raise ValueError('Password can not start or end with blank spaces')
        return value

#response
class Token(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str


#submit
class RefreshToken(BaseModel):
    refresh_token:str

#response
class AccessToken(BaseModel):
    access_token:str
    token_type:str





