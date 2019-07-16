from flask_restplus import Api, Resource
from flask import Flask, request
from Model import Employee, db, EmployeeSchema, Company, CompanySchema
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app, version='1.0', title='Employee API',description='Employee API')
ns = api.namespace('tables', description='Employees related operations')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
company_schema = CompanySchema()
db_uri = "postgresql+psycopg2://postgres:root@localhost/postgres"
engine = create_engine(db_uri)

@ns.route('/')
class Tables(Resource):
    changed_generated_id = 0

    def post(self):
        json_data = request.get_json(force=True)
        self.get_the_right_table(json_data)

    def get_the_right_table(self, json_data):
        master_data = {}
        for data in json_data['data']:
            if data['Table'] not in master_data.keys():
                master_data[data['Table']] = []
            master_data[data['Table']].append(data['data'])

        master_data_id = {}
        for keys in range(len(master_data.get('company'))):
            master_data_id[master_data.get('company')[keys]['company_id']] = []
            self.post_company_data(keys, master_data.get('company'), master_data_id)

        for key in range(len(master_data.get('employee'))):
            self.post_employee_data(key, master_data.get('employee'), master_data_id)

        #for keys in range(len(master_data.get('company'))):
            #for keys2 in range(len(master_data.get('employee'))):
                #comp_id = master_data.get('company')[keys]['company_id']
                #emp_id = master_data.get('employee')[keys2]['company_id']

                #company_object = Company.query.get(comp_id)
                #company_object = company_schema.dump(company_object).data
                #employee_object = Employee.query.get(emp_id)
                #employee_object = employee_schema.dump(employee_object).data

                #if comp_id == emp_id and bool(company_object) is False and bool(employee_object) is False:
                  #  result = self.post_company_data(keys, master_data.get('company'))
                   # self.post_employee_data(keys2, master_data.get('employee'), result)

                #if bool(employee_object) is False and bool(company_object) is True:
                 #   self.post_employee_data(keys2, master_data.get('employee'))

                #if bool(company_object) is False:
                 #   self.post_company_data(keys, master_data.get('company'))

    def post_company_data(self, keys, json_data, master_data_id):
        changed_generated_id = json_data[keys]['company_id']
        company_object = Company.query.get(changed_generated_id)
        company_object = company_schema.dump(company_object).data

        if not company_object:
            company = Company(
                name=json_data[keys]['name'],
                )
            db.session.add(company)
            db.session.commit()
            changed_generated_id = company_schema.dump(company).data
            master_data_id[json_data[keys]['company_id']].append(changed_generated_id['id'])
        return master_data_id

    def post_employee_data(self, keys2, json_data, master_data_id):
        changed_generated_id = json_data[keys2]['company_id']
        print(bool(master_data_id.get(changed_generated_id)))
        print(master_data_id.keys())
        if bool(master_data_id.get(changed_generated_id)):
            company_id = int("".join(list(map(str, master_data_id.get(changed_generated_id)))))
        else:
            company_id = json_data[keys2]['company_id']
        employee_object = Employee.query.get(changed_generated_id)
        employee_object = employee_schema.dump(employee_object).data

        if not employee_object:
            employee = Employee(
                name=json_data[keys2]['name'],
                email=json_data[keys2]['email'],
                company_id=company_id
            )
            db.session.add(employee)
            db.session.commit()
        changed_generated_id = employee_schema.dump(employee).data
        return changed_generated_id['id']
