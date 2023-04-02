import json
from pprint import pprint
from functools import lru_cache


@lru_cache
def get_companies():
    with open('mini-data/companies.json') as jsonfile:
        return json.load(jsonfile, parse_int=str)
        #json.load({???}, parse_int=str)
        #pprint(companies)


@lru_cache
def get_contracts():
    with open('mini-data/conracts1.json') as jsonfile:
        return json.load(jsonfile, parse_int=str)
        #pprint(contracts)

@lru_cache
def get_participants():
    with open('mini-data/participants.json') as jsonfile:
        return json.load(jsonfile, parse_int=str)
        #pprint(participants)

@lru_cache
def get_purchases():
    with open('mini-data/purchases.json') as jsonfile:
        return json.load(jsonfile, parse_int=str)
        #pprint(purchases)

# def find_company(tin: str):

#     return 