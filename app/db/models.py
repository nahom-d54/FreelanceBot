from telegram import Update
from telegram.ext import CallbackContext
from .db import connectDb
from bson import ObjectId


class User:
    def __init__(self, collection) -> None:
        #self.collection = context.bot_data['collection']['user']
        self.collection = collection['user']
    async def insertUser(self, user: Update):
        first_name = user.message.chat.first_name
        last_name = user.message.chat.last_name
        _id = user.effective_user.id
        username = user.effective_user.username

        user_to_insert = {
            "_id": _id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username
        }
        if not await self.__exists__(_id):
            await self.collection.insert_one(user_to_insert)
    async def updateUser(self, _id, query):
        await self.collection.update_one(
            {"_id": _id},
            {"$set": query}
        )
    async def deleteUser(self, _id):
       await self.collection.delete_one(
            {"_id": _id}
        ) 
    async def getUser(self, _id):
        exists = await self.collection.find_one({"_id": _id})

        return exists
    
    async def __exists__(self, _id):
        exists = await self.getUser(_id)

        if exists:
            return True
        else:
            return False
class Job:
    def __init__(self, collection) -> None:
       self.collection = collection['job'] 
       
    async def createJobListing(self, job, _id):
        job_to_insert = {
            "user": _id,
            "approval": {
                "status": "Pending",
                "approved": False
            }
        }
        job_to_insert.update(job)

        inserted = await self.collection.insert_one(job_to_insert)
        this = await self.findJobByJobId(inserted.inserted_id)

        return this
    
    async def findJobByJobId(self, job_id):
        job = await self.collection.find_one({"_id": ObjectId(job_id)})

        return job
class Company:
    def __init__(self, collection) -> None:
       self.collection = collection['company'] 
       
    async def insertCompany(self, company, _id):
        company_to_insert = {
            "user": _id,
            "verified": {
                "status": False
            }
        }
        company_to_insert.update(company)

        await self.collection.insert_one(company_to_insert)

    async def getCompanyByUser(self, _id):
        companies = self.collection.find({"user": _id})

        return await companies.to_list(length = 15)
    async def getCompanyById(self, company_id):
        return await self.collection.find_one({"_id": ObjectId(company_id)})
        



collection = connectDb()

class CC(CallbackContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.User = User(collection)
        self.Job = Job(collection)
        self.Company = Company(collection)