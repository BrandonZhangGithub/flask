from App.settings import REDIS
#cache 自带redis的链接方法
class CacheConfig():
    CACHE_TYPE ='redis'
    CACHE_REDIS_HOST = REDIS.GET('host')
    CACHE_REDIS_PORT = REDIS.GET('port')
    CACHE_REDIS_PASSWORD = REDIS.GET('pwd')
    CACHE_REDIS_DB = 1


