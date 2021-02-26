from flask_restful import Resource

class IndexView(Resource):
    def get(self):
        return {'greeting': 'Hello, DevGrid!'}
