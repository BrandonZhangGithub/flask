import os
from flask_restful import Resource
from flask import request
class upload(Resource):
    def post(self):
        file = request.files.get('file')
        basepath = os.path.dirname(os.path.dirname(__file__))
        upPath = "statics/uploads/imgs"
        path = os.path.join(basepath,upPath,file.filename)
        file.save(path)
        return 'ok'
