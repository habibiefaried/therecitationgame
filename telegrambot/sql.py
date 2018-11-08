import pymongo
from pprint import pprint

f = open("../secrets/mongouser", "r")
mongouser = f.read()
f = open("../secrets/mongopass", "r")
mongopass = f.read()
f = open("../secrets/mongohost", "r")
mongohost = f.read()

client = pymongo.MongoClient("mongodb://"+mongouser+":"+mongopass+"@"+mongohost+"/test")
db = client.test

pprint(db)
