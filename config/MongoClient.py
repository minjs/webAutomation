from pymongo import MongoClient


class MongoClient:

    mongoClient = None

    def __init__(self, server='127.0.0.1', port=27017):
        self.mongoClient = MongoClient(server, port)

    def insert(self, db, collection, data):
        self.mongoClient[db][collection].insert(data)

    def upsert(self, db, collection, pattern, data):
        self.mongoClient[db][collection].update(pattern, data, upsert=True)

    def query(self, db, collection, pattern=None):
        if pattern is None:
            return self.mongoClient[db][collection].find()
        else:
            return self.mongoClient[db][collection].find(pattern)

    def collection_names(self, db, include_system_collections=False):
        return self.mongoClient[db].collection_names(include_system_collections=include_system_collections)

    def find_distinct_list(self, db, collection, key, filter=None):
        return self.mongoClient[db][collection].distinct(key, filter=filter)