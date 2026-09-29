from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from app.db.database import client


import time
import uuid 



from app.routes.users import router as user_router
from app.routes.notes import router as notes_router
from app.routes.admin import router as admin_router




@asynccontextmanager
async def lifespan(app:FastAPI):
    result=await client.admin.command('ping')
    print(result)
    print('Sucessfuly connected')

    yield

    await client.close()

app= FastAPI(lifespan=lifespan)

#TODO MIDDLEWARES

#ADD CORS,TRUSTED HOST,HTTPS REDIRECT,GZIP LATER


#TIMING REQUEST
@app.middleware('http')
async def timing_middleware(request:Request,call_next):
    start=time.perf_counter()

    response= await call_next(request)
    response.headers['X-my-header']='hello'

    duration=time.perf_counter()-start

    print(f'Method->{request.method} URL->{request.url.path} DURATION->{duration:4f}s')

    return response

#REQUEST ID LOGGER

@app.middleware('http')
async def request_id_logger(request:Request,call_next):
    request_id=str(uuid.uuid4())

    print(f'Request Start->{request_id}')
    response=await call_next(request)

    response.headers['X-Request-ID']=request_id

    print(f'Request end-> {request_id}')
    return response




app.include_router(user_router)
app.include_router(notes_router)
app.include_router(admin_router)

