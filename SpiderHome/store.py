import pymongo

client = pymongo.MongoClient('localhost', 27017)
GdsqDB = client.GdsqDB
GDSWDB = client.GDSWDB
GZSSDB = client.GZSSDB
CSGHDB1 = client.CSGHDB1
CSGHDB2 = client.CSGHDB2
GDEPBDB = client.GDEPBDB
GdszDB = client.GdszDB
