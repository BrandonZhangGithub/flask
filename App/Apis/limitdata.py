from flask_restful import Resource
from App.models import User,Order
from App import db
from flask import jsonify

#RESTful必须使用类的方式创建接口
#RESTful独立设置路由

class Ldata(Resource):
    def get(self):
        return jsonify({'code':200,'content':'get接口'})
    def post(self):
        return jsonify({'code': 200, 'content': 'post接口'})

#flask-bootstrap  前端框架 css js
#