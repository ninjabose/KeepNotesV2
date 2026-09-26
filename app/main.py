from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import client

from app.routes.users import router as user_router
from app.routes.notes import router as notes_router




@asynccontextmanager
async def lifespan(app:FastAPI):
    result=await client.admin.command('ping')
    print(result)
    print('Sucessfuly connected')

    yield

    await client.close()

app= FastAPI(lifespan=lifespan)

#TODO MIDDLEWARES

app.include_router(user_router)
app.include_router(notes_router)

