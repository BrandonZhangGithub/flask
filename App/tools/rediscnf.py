from App.settings import REDIS
from redis import ConnectionPool,Redis
class RedisConnection():
    def conn(host=REDIS['host'],port=REDIS['port'],pwd=REDIS['pwd'],db=REDIS['db'],decode_response=False):
        pools = ConnectionPool(
            host = host,
            port = port,
            password = pwd,
            db = db,
            #默认utf-8
            decode_responses = decode_response
        )
        Redis(connection_pool=pools)


