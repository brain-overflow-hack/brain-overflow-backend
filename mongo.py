from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from mini_data import *
from datetime import datetime, timedelta

class _MongoWrapper:
    def __init__(self) -> None:
        url = "mongodb://root:root@mongo:27017"
        self.db: AsyncIOMotorDatabase = AsyncIOMotorClient(url)["db"]

        self.companies: AsyncIOMotorCollection = self.db["companies"]
        self.purchases: AsyncIOMotorCollection = self.db["purchases"]
        self.contracts: AsyncIOMotorCollection = self.db["contracts"]
        self.participants: AsyncIOMotorCollection = self.db["participants"]

    async def fill_db(self):
        if await self.companies.count_documents({}) == 0:
            await self.companies.insert_many(get_companies())

        if await self.purchases.count_documents({}) == 0:
            await self.purchases.insert_many(get_purchases())

        if await self.contracts.count_documents({}) == 0:
            await self.contracts.insert_many(get_contracts())

        if await self.participants.count_documents({}) == 0:
            await self.participants.insert_many(get_participants())
        return None
    
    async def find_company(self, tin: str):
        if company := await self.companies.find_one({"supplier_inn": tin}, {'_id': 0}):
            return company
        raise ValueError

    async def find_fake_data(self):
        return await self.contracts.count_documents({"contract_conclusion_date": "1970-01-01"})
    
    async def get_chart_data_win(self, tin: str):
        end_date = datetime.now().replace(day=1) # First day of the current month
        start_date = end_date - timedelta(days=360*3) # last 6 months

        # Initialize a dictionary to store the results for each month
        results = {}

        # Loop through each month in the date range
        while end_date > start_date:
            # Format the dates for the current month
            end_date_str = end_date.strftime('%Y-%m-%d')
            start_date_str = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
            month_year_str = end_date.strftime('%m-%Y')

            # Query the database to get the count of contracts for the current month
            count = await self.contracts.count_documents({
                '$and': [
                    {'contract_conclusion_date': {'$gte': start_date_str, '$lt': end_date_str}},
                    {'id': {'$in': [p['id'] for p in await self.participants.find({'supplier_inn': tin, 'is_winner': 'Да'}).to_list(length=None)]}}
                ]
            })

            # Store the result for the current month
            results[month_year_str] = count

            # Move to the previous month
            end_date = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1)

        # Return the results in the required format
        result = {'supplier_inn': tin, 'date_range': f'{start_date_str} to {end_date_str}', 'counts': results}
        #data = {'labels': [], 'datasets': [ {'labels'} ]}
        data = []
        labels = []
        for month, cnt in result['counts'].items():
            labels.append(month)
            data.append(cnt)
        chart_data = {'labels': labels, 'datasets': [{'label': 'Wins for month', 'data': data , 'backgroundColor': '#f87979'}]}
        return chart_data
    
    async def get_chart_data_all(self, tin: str):
        end_date = datetime.now().replace(day=1) # First day of the current month
        start_date = end_date - timedelta(days=360*3) # last 6 months

        # Initialize a dictionary to store the results for each month
        results = {}

        # Loop through each month in the date range
        while end_date > start_date:
            # Format the dates for the current month
            end_date_str = end_date.strftime('%Y-%m-%d')
            start_date_str = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
            month_year_str = end_date.strftime('%m-%Y')

            # Query the database to get the count of contracts for the current month
            count = await self.contracts.count_documents({
                '$and': [
                    {'contract_conclusion_date': {'$gte': start_date_str, '$lt': end_date_str}},
                    {'id': {'$in': [p['id'] for p in await self.participants.find({'supplier_inn': tin}).to_list(length=None)]}}
                ]
            })

            # Store the result for the current month
            results[month_year_str] = count

            # Move to the previous month
            end_date = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1)

        # Return the results in the required format
        result = {'supplier_inn': tin, 'date_range': f'{start_date_str} to {end_date_str}', 'counts': results}
        #data = {'labels': [], 'datasets': [ {'labels'} ]}
        data = []
        labels = []
        for month, cnt in result['counts'].items():
            labels.append(month)
            data.append(cnt)
        chart_data = {'labels': labels, 'datasets': [{'label': 'Participations for month', 'data': data , 'backgroundColor': '#f87979'}]}
        return chart_data
    
    async def get_chart_data_sum(self, tin: str):
        end_date = datetime.now().replace(day=1) # First day of the current month
        start_date = end_date - timedelta(days=360*3) # last 6 months

        # Initialize a dictionary to store the results for each month
        results = {}

        # Loop through each month in the date range
        while end_date > start_date:
            # Format the dates for the current month
            end_date_str = end_date.strftime('%Y-%m-%d')
            start_date_str = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
            month_year_str = end_date.strftime('%m-%Y')

            # Query the database to get the count of contracts for the current month
            docs = await self.contracts.find({
                '$and': [
                    {'contract_conclusion_date': {'$gte': start_date_str, '$lt': end_date_str}},
                    {'id': {'$in': [p['id'] for p in await self.participants.find({'supplier_inn': tin}).to_list(length=None)]}},
                ]
            }).to_list(length=None)

            month_sum = 0

            for doc in docs:
                month_sum += doc['price']

            # Store the result for the current month
            results[month_year_str] = month_sum

            # Move to the previous month
            end_date = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1)

        # Return the results in the required format
        result = {'supplier_inn': tin, 'date_range': f'{start_date_str} to {end_date_str}', 'sum': results}
        #data = {'labels': [], 'datasets': [ {'labels'} ]}
        data = []
        labels = []
        for month, sum in result['sum'].items():
            labels.append(month)
            data.append(sum)
        chart_data = {'labels': labels, 'datasets': [{'label': 'Sum for month', 'data': data , 'backgroundColor': '#f87979'}]}
        return chart_data

Mongo = _MongoWrapper()