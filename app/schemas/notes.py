from pydantic import BaseModel,Field,ConfigDict
from pydantic.functional_serializers import PlainSerializer
from datetime import datetime
from enum import Enum
from typing import Annotated
from bson import ObjectId


Title=Annotated[str,Field(min_length=1,max_length=50)]
Body=Annotated[str,Field(min_length=1,max_length=500)]
Tags=Annotated[list[str],Field()]

PyID=Annotated[ObjectId,PlainSerializer(str,return_type=str)]

class Status(str,Enum):
    DRAFT='draft'
    PUBLISHED='published'
    ARCHIVED='archived'

class Visibility(str,Enum):
    PRIVATE='private'
    LIST='list'
    FRIENDS='friends'
    PUBLIC='public'


class CreateNote(BaseModel):
    title:Title
    body:Body

    status:Status=Field(default=Status.DRAFT)
    visibility:Visibility=Field(default=Visibility.PRIVATE)

    tags:Tags=Field(default_factory=list)

    #created_at:datetime
    #updated_at:datetime

    model_config=ConfigDict(extra='forbid')


class ResponseNote(BaseModel):
    id:PyID=Field(alias='_id')
    title:Title
    body:Body

    status:Status
    visibility:Visibility
    tags:Tags

    created_at:datetime
    updated_at:datetime

    author_id:PyID


class EditNote(BaseModel):

    title:Title|None=None
    body:Body|None=None

    status:Status|None=None
    visibility:Visibility|None=None

    tags:Tags|None=None

    #created_at:datetime
    #updated_at:datetime

    model_config=ConfigDict(extra='forbid')







