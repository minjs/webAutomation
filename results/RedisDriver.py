import redis


class RedisDriver:

    redisDriver = None


    def __init__(self, server='127.0.0.1', port=6379):
        self.redisDriver = redis.StrictRedis(server=server, port=port)
