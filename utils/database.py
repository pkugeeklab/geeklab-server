from pymongo import MongoClient

client = None
db = None


def load():
    global client
    global db
    client = MongoClient('localhost', 27017)
    db = client.geeklab
