import pymongo

client = pymongo.MongoClient('localhost', 27017)
GdsqDB = client.GdsqDB
GDSWDB = client.GDSWDB
GZSSDB = client.GZSSDB
