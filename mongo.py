from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from mini_data import *

class _MongoWrapper:
    def __init__(self) -> None:
        url = "mongodb://root:root@mongo:27017"
        self.db: AsyncIOMotorDatabase = AsyncIOMotorClient(url)["db"]

        self.companies: AsyncIOMotorCollection = self.db["companies"]
        self.purchases: AsyncIOMotorCollection = self.db["purchases"]
        self.contracts: AsyncIOMotorCollection = self.db["contracts"]
        self.partisipants: AsyncIOMotorCollection = self.db["partisipants"]

    async def fill_db(self):
        if await self.companies.count_documents({}) == 0:
            await self.companies.insert_many(get_companies())
        return None
    
    async def find_company(self, tin: str):
        if company := await self.companies.find_one({"supplier_inn": tin}, {'_id': 0}):
            return company
        raise ValueError

Mongo = _MongoWrapper()