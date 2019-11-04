from flask_restful import Api
from .Apis.limitdata import Ldata
from App.Apis.upload import Upload

api = Api()
def init_urls(app):
    #add_resource 添加一个路由
    app.add_resource(Ldata,'/limit/')
    api.init_app(app=app)
    api.add_resource(Upload,'/upload/')

