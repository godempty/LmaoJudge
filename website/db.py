import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb+srv://alanlai:mG1Jx8TEknjqo09c@cluster0.i1iaccu.mongodb.net/?retryWrites=true&w=majority")

db = cluster['lmaojudge']
