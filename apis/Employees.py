from flask_restplus import Api, Resource, fields, reqparse
from Model import Employee, EmployeeSchema, db,Company
from flask import request, jsonify, abort, Flask
import logging


app = Flask(__name__)
api = Api(app, version='1.0', title='Employee API',description='Employee API')
ns = api.namespace('employee', description='Employees related operations')

employees_schema = EmployeeSchema(many=True)
employee_schema = EmployeeSchema()
logger = logging.getLogger()


def get_paginated_list(data, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(data)
    if count < start or limit < 0:
        abort(404)

    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

    obj['data'] = data[(start - 1):(start - 1 + limit)]
    return obj


parser = reqparse.RequestParser()
parser.add_argument('employee_id', type=str, required=True, help='input is mandatory')
@ns.route('/')
class EmployeeList(Resource):
    @ns.doc('list_employees')
    @ns.expect(parser)
    def get(self):
        logger.info('Get request for employees')
        employee = Employee.query.all()
        employee = employees_schema.dump(employee).data
        #join tables and return accordingly
        query = db.session.query(Employee, Company).join(Company)
        print(query.filter(Company.id == Employee.company_id).all())
        return {"status": "done", "data": employee}
        #jsonify(get_paginated_list(
         #   employee,
          #  '/employee',
          #  request.args.get('start', 1),
           # request.args.get('limit', 20)
        #))

    resource_fields = ns.model('data', {
        'name': fields.String,
        'email': fields.String
    })
    @ns.doc('post_employees')
    @ns.expect([resource_fields], validate=True)
    def post(self):
        json_data = request.get_json(force=True)
        employee = Employee(
            name=json_data['name'],
            email=json_data['email'],
            company_id=json_data['company_id']
            )
        db.session.add(employee)
        db.session.commit()
        result = employee_schema.dump(employee).data
        return {"status": 'success', 'data': result}, 201

    @ns.doc('delete_employees')
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = employee_schema.load(json_data)
        if errors:
            return errors, 422
        employee = Employee.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = employee_schema.dump(employee).data

        return {"status": "success", "data": result}, 204

    @ns.doc('patch_employees')
    def patch(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        data, errors = employee_schema.load(json_data)
        if errors:
            return errors, 422
        employee = Employee.query.filter_by(id=data['id']).first()
        employee.name = data['name']
        employee.email = data['email']
        db.session.commit()

        result = employee_schema.dump(employee).data

        return {"status": "success", "data": result}, 201

