from .rediscnf import RedisConnection
class SessionConfig():
    #密钥
    SECRET_KEY = '10086'
    #选择session的存储位置
    SESSION_TYPE = 'redis'
    #session在存储时给key值加上前缀
    SESSION_KEY_PREFIX = 'Flask_'
    #建立redis的链接
    SESSION_REDIS = RedisConnection.conn(db=15)

