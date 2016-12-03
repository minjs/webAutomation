from config.Config import Config


'''
    Configuration example
    {
        "username": "mren",
        "website": "dealsea.com",
        "keyword": "macy's",
        "start":  "",
        "expire":  ""
    }
'''


class DbConfig(Config):

    def __init__(self):
        Config.__init__()

    def get_keywords_list(self, website):
        return self.mongoClient.find_distinct_list(self.dbName, website, "keyword")

    '''
        return a timing valid keyword list per user
    '''
    def get_user_keywords_list(self, website, user):
        return self.mongoClient.find_distinct_list(self.dbName, website, "username", filter={"username": user})

