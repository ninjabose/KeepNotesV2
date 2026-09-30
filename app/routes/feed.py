from fastapi import APIRouter,Depends,HTTPException,Query
import logging


from app.db.database import db
from app.core.security import get_current_user
from app.schemas.notes import Visibility,Status,FeedResponse
from app.services.cursor import encode_cursor,decode_cursor



router=APIRouter(prefix='/feed',tags=['feed'])
logger=logging.getLogger(__name__)


#status->published
#visibility->public

@router.get('/explore')
async def explore_notes(user:dict=Depends(get_current_user),
                        page:int=Query(1,ge=1),
                        limit:int=Query(10,ge=10)
                        ):
    #FIXED QUERY
    query={
        'status':Status.PUBLISHED.value,
        'visibility':Visibility.PUBLIC.value
    }

    #CURSOR
    cursor = db.notes.find(query)

    #SORT
    cursor.sort('created_at',-1)

    skip=(page-1)*limit
    cursor=cursor.limit(limit).skip(skip)

    feed_notes=await cursor.to_list()

    return feed_notes

#Let's use cursor to scale.. it's not mongo db cursor .. both have same name but are different things

'''
@router.get('/explore/scale',response_model=list[ResponseNote])
async def explore_notes(user:dict=Depends(get_current_user),
                        cursor_created_at:datetime|None=None,
                        cursor_id:str|None=None,
                        limit:int=Query(10,ge=1,lt=100)
                        ):
    #FIXED QUERY
    query={
        'status':Status.PUBLISHED.value,
        'visibility':Visibility.PUBLIC.value
    }

    # If this isn't the first request, continue after the cursor
    if cursor_created_at is not None and cursor_id is not None:
        query['$or']=[
            {
                'created_at':{
                    '$lt':cursor_created_at
                    }
            },
            {
                'created_at':{
                    '$lt':ObjectId(cursor_id)
                }
            }
        ]

    notes_cursor=(
        db.notes.find(query)
        .sort([
            ('created_at',-1),
            ('_id',-1)
        ])
        .limit(limit+1)
        )

    feed_notes= await notes_cursor.to_list(limit=limit+1)
    return feed_notes
    '''

@router.get("/explore", response_model=FeedResponse)
async def explore_notes(
    user: dict = Depends(get_current_user),
    cursor: str | None = None,
    limit: int = Query(10, ge=1, le=100),
):
    query = {
        "status": Status.PUBLISHED.value,
        "visibility": Visibility.PUBLIC.value,
    }

    if cursor:
        cursor_created_at, cursor_id = decode_cursor(cursor)

        query["$or"] = [
            {
                "created_at": {
                    "$lt": cursor_created_at
                }
            },
            {
                "created_at": cursor_created_at,
                "_id": {
                    "$lt": cursor_id
                }
            }
        ]

    db_cursor = (
        db.notes
        .find(query)
        .sort([
            ("created_at", -1),
            ("_id", -1)
        ])
        .limit(limit + 1)
    )

    notes = await db_cursor.to_list(limit=limit + 1)

    has_more = len(notes) > limit

    if has_more:
        notes.pop()

    next_cursor = None

    if has_more and notes:
        last_note = notes[-1]

        next_cursor = encode_cursor(
            last_note["created_at"],
            last_note["_id"]
        )

    return {
        "items": notes,
        "next_cursor": next_cursor
    }





