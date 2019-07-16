from flask_restplus import Api, Resource, fields
from Model import Company, CompanySchema, db
from flask import request, Flask
import logging

app = Flask(__name__)
api = Api(app, version='1.0', title='Company API',description='Company API')
ns = api.namespace('company', description='Company related operations')

companies_schema = CompanySchema(many=True)
company_schema = CompanySchema()
logger = logging.getLogger()


@ns.route('/')
class CompanyList(Resource):
    @ns.doc('list_company')
    def get(self):
        logger.info('Get request for company')
        company = Company.query.all()
        company = companies_schema.dump(company).data
        return {'status': 'done', 'done': company}

    resource_fields = ns.model('data', {
        'name': fields.String,
    })

    @ns.doc('post_company')
    @ns.expect([resource_fields], validate=True)
    def post(self):
        json_data = request.get_json(force=True)
        employee = Company(
            name=json_data['name']
            )
        db.session.add(employee)
        db.session.commit()
        result = company_schema.dump(employee).data
        return {"status": 'success', 'data': result}, 201

