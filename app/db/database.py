from app.core.config import settings
from pymongo import AsyncMongoClient

MONGODB_URI=settings.MONGODB_URI
client=AsyncMongoClient(MONGODB_URI)

db=client[settings.DATABASE_NAME]



