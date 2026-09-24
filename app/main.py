from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import client


@asynccontextmanager
async def lifespan(app:FastAPI):
    result=await client.admin.command('ping')
    print(result)
    print('Sucessfuly connected')

    yield

    await client.close()

app= FastAPI(lifespan=lifespan)