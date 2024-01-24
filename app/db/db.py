#import pymongo
# using motor for asyncronous process
from motor.motor_asyncio import AsyncIOMotorClient
from telegram import Update
from ..config import Config

def connectDb():
    try:
        # connection = pymongo.MongoClient("mongodb://localhost:27017/")
        connection = AsyncIOMotorClient(Config.MONGODB_URI)
        collection = connection["marosetclone"]
        return collection
    except Exception as e:
        raise Exception(e)


