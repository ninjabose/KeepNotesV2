from pydantic import BaseModel,Field,EmailStr



class UserCred(BaseModel):
    username:str=Field(min_length=3,max_length=50)
    firstname:str
    lastname:str
    email:EmailStr
    password:str

