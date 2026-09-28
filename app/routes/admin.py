from fastapi import APIRouter,Depends,Query
from datetime import datetime,timezone,timedelta



from app.db.database import db
from app.core.security import get_current_admin





router= APIRouter(prefix='/admin',tags=['admin'])

@router.get('/get_count')
async def get_stats_notes(user:dict=Depends(get_current_admin)):

    user_count=await db.users.count_documents({})
    notes_count=await db.notes.count_documents({})

    return{
        'user_count': user_count,
        'notes_count':notes_count
    }


#Aggregation pipeline 
#AND
#lookup

@router.get('/notes_per_user')
async def get_notes_per_user(user:dict=Depends(get_current_admin),limit:int=Query(5,ge=5)):
    pipeline=[
        {
        '$group':{
        '_id':'$author_id',
        'total_notes':{'$sum':1}}
        },    
        {
        '$lookup':{
        'from':'users',
        'localField':'_id',
        'foreignField':'_id',
        'as':'user'
        }},
        {
        '$sort':{'total_notes':-1}
        },
        {
        '$limit':limit
        },
        {
        '$project':{
        '_id':0,
        'user_id':{'$toString':'$_id'},
        'name':{'$arrayElemAt':['$user.name',0]},
        'total_notes':1
        }
        }]
    cursor=await db.notes.aggregate(pipeline)
    result=await cursor.to_list()

    return result


#Full aggregation pipeline

@router.get('/notes_per_year')
async def get_notes_per_year(user:dict=Depends(get_current_admin),
                             limit:int=Query(10,ge=10),
                             start:datetime=Query(datetime.now(timezone.utc)-timedelta(days=365),gte=datetime(2000,1,1,tzinfo=timezone.utc)),
                             end:datetime=Query(datetime.now(timezone.utc),lt=datetime(3000,1,1,tzinfo=timezone.utc))
                             ):
    pipeline=[{
        '$match':{
            'updated_at':{'$exists':True},
            'created_at':{'$gte':start,'$lt':end}
        }},
        {
            '$group':{
                '_id':{'$year':'$created_at'},
                'total_notes':{'$sum':1}
            }
        },
        {
            '$sort':{'total_notes':-1} #try year also
        },
        {
            '$limit':limit
        },
        {
            '$project':{
                '_id':0,
                'year':'$_id',
                'total_notes':1
            }
        }

    ]

    cursor=await db.notes.aggregate(pipeline)
    result=await cursor.to_list()
    return result
    
    





