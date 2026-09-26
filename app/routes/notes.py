from fastapi import APIRouter,Depends,HTTPException,Query
from datetime import datetime,timezone,timedelta
import logging
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Literal
import re


from app.db.database import db
from app.core.security import get_current_user
from app.schemas.notes import CreateNote,ResponseNote,EditNote


router=APIRouter(prefix='/notes',tags=['notes'])
logger=logging.getLogger(__name__)


@router.post('/',response_model=ResponseNote)
async def create_note(note_input:CreateNote,user:dict=Depends(get_current_user)):
    note=note_input.model_dump()
    note.update(
        {
            'author_id':user['_id'],
            'created_at': datetime.now(timezone.utc),
            'updated_at':datetime.now(timezone.utc)
        }
    )
    try:
        result=await db.notes.insert_one(note)
    except Exception as e:
        logger.exception(f'Fail Note Create -> {e}')
        print(f'Fail Note Create -> {e}')
        

        raise HTTPException(
            status_code=500,
            detail='Internal Server Error'
        )

    note['_id']=result.inserted_id
    return note

@router.patch('/{note_id}',response_model=ResponseNote)
async def edit_note(note_id:str,note_input:EditNote,user:dict=Depends(get_current_user)):

    try:
        note_obj_id=ObjectId(note_id)
    except:
        raise HTTPException(
            status_code=400,
            detail='Bad request'
        )
    note=note_input.model_dump(exclude_unset=True)
    note['updated_at']=datetime.now(timezone.utc)
    query={
        '_id':note_obj_id,
        'author_id':user['_id']
    }
    result=await db.notes.find_one_and_update(
        query,
        {'$set':note},
        return_document=ReturnDocument.AFTER
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail='Note not found'
        )
    return result

@router.get('/',response_model=list[ResponseNote])
async def get_notes(
    user:dict=Depends(get_current_user),
    search:str|None=None,
    filter_year:int|None=None,
    sort:Literal['-time','time']='-time',
    page:int=Query(1,ge=1),
    limit:int=Query(5,ge=5)):

    #USER ID
    query={'author_id':user['_id']}

    #SEARCH
    if search:
        search=re.escape(search)
        query['$or']=[
            {'title':{'$regex':search,'$options':'i'}},
            {'body':{'$regex':search,'$options':'i'}}
        ]
    #YEAR
    if filter_year:
        start=datetime(filter_year,1,1,tzinfo=timezone.utc)
        end=datetime(filter_year+1,1,1,tzinfo=timezone.utc)

        query['created_at']={'$gte':start,'$lt':end}

    #CREATE CURSOR
    cursor=db.notes.find(query)

    #SORT BY TIME 

    if sort=='-time':
        cursor.sort('created_at',-1)
    else:
        cursor.sort('created_at',+1)

    #PAGINATION

    skip=(page-1)*limit #offset
    cursor=cursor.skip(skip).limit(limit)


    all_notes=await cursor.to_list(length=limit)

    return all_notes

@router.delete('/{note_id}',status_code=204)
async def delete_note(note_id:str,user:dict=Depends(get_current_user)):
    try:
        note_obj_id=ObjectId(note_id)
    except TypeError:
        raise HTTPException(
            status_code=400,
            detail='Bad request'
        )
    query={'_id':note_obj_id,'owner_id':user['_id']}
    delete=await db.notes.find_one_and_delete(query)
    if not delete:
        raise HTTPException(
            status_code=404,
            detail='Note not found'
        )










    


