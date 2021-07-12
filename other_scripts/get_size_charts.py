import pymongo
import json


text = open("mongo_uri.txt", "r")
mongo_uri = text.read().strip()
text.close()
mongo_db = "remotasks"
client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]

results = db["adidas"].find().distinct("size_chart_link")
print(results)