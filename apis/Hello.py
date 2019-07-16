from flask_restplus import Api, Resource
from flask import Flask

app = Flask(__name__)
api = Api(app, version='1.0', title='Employee API',description='Employee API')
ns = api.namespace('hello', description='Hello World Example')


HELLO = {'id':'1','name':'shubham','email':'shubham@example.com'}


@ns.route('/')
class EmployeeList(Resource):
    @ns.doc('hello_world')
    def get(self):
        return HELLO
