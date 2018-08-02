import Flask from flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'helloworld': 'fromapi.py'}

api.add_resource(HelloWorld, '/')