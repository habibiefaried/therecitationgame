import pymongo
from pprint import pprint

f = open("/var/run/secrets/mongouser", "r")
mongouser = f.read()
f = open("/var/run/secrets/mongopass", "r")
mongopass = f.read()
f = open("/var/run/secrets/mongohost", "r")
mongohost = f.read()

client = pymongo.MongoClient("mongodb://"+mongouser+":"+mongopass+"@"+mongohost+"/test")
db = client.test

pprint(db)
