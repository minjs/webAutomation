from config.MongoClient import MongoClient


class Config:
    dbName = "monitor"
    mongoClient = None
    userCollection = "users"

    def __init__(self):
        self.mongoClient = MongoClient()

    def get_website_list(self):
        return self.mongoClient.collection_names(self.dbName)

    def get_user_list(self, website):
        return self.mongoClient.find_distinct_list(self.dbName, website, "username")

    def get_user_contact(self, user):
        return self.mongoClient.query(self.dbName, self.userCollection, pattern={"username": user})

    def insert_config(self, website, config):
        self.mongoClient.insert(self.dbName, website, config)

    def update_config(self, website, config, pattern):
        self.mongoClient.upsert(self.dbName, website, pattern, config)
