from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return {'greeting': 'Hello, DevGrid!'}

api.add_resource(Index, '/')
