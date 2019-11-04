from flask import Flask
from .tools.sessioncnf import SessionConfig
from flask_session import Session
#flask session pip install flask_session -i https://pypi.douban.com/simple
from flask_sqlalchemy import SQLAlchemy
from .tools.mysqlcnf import MysqlConfig
from .tools.cachecnf import CacheConfig
from flask_cache import Cache
cache = Cache()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #读取配置文件
    app.config.from_object(SessionConfig)
    #动态加载
    Session(app=app)

    #把flask-sqlachemy的配置项导入到app
    app.config.from_object(MysqlConfig)
    #动态加载
    db.init_app(app=app)

    #pip imstall flask-cache
    #cache需要配置内存　redis
    #在jinjia2删除 .exit 改成flask_cache
    app.config.from_object(CacheConfig)
    cache.init_app(app=app)
    return app

