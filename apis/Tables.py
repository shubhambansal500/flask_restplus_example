from flask_restplus import Api, Resource
from flask import Flask, request
from Model import Employee, db, EmployeeSchema, Company, CompanySchema

app = Flask(__name__)
api = Api(app, version='1.0', title='Employee API', description='Employee API')
ns = api.namespace('tables', description='Employees related operations')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
company_schema = CompanySchema()


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

        model_finder = {
            "company": (Company, company_schema),
            "employee": (Employee, employee_schema)
        }

        master_data_sorted = self.get_sorted_master_data(master_data)

        master_data_id = {}
        pk_prop_name = 'M_COMPANY_ID'
        master_data_id[pk_prop_name.upper()] = []
        for keys, values in master_data_sorted.items():
            print(keys, values)
            for value in values:
                model, schema = model_finder.get(keys)
                self.insert_record(value, model, schema, master_data_id)
                print(value)

    def get_sorted_master_data(self, master_data):
        master_data_unsorted = master_data
        key_order = ['admin', 'company', 'employee']
        master_data_sorted = dict(sorted(master_data_unsorted.items(), key=lambda i: key_order.index(i[0])))
        print(dict(master_data_sorted))
        return master_data_sorted

    def insert_record(self, json_data, model_type, schema_obj, master_data_id):

        #master_data_id[pk_prop_name.upper()].append(json_data[pk_prop_name.upper()])
        if not master_data_id['M_COMPANY_ID']:
            master_data_id['M_COMPANY_ID'].append(json_data['M_COMPANY_ID'])

        elif int("".join(list(map(str, master_data_id['M_COMPANY_ID'])))) == json_data['M_COMPANY_ID']:
            json_data['M_COMPANY_ID'].append(int("".join(list(map(str, master_data_id['M_COMPANY_ID'])))))


        new_object = schema_obj.dump(json_data).data
        new_obj = model_type(**new_object)
        db.session.add(new_obj)
        db.session.commit()
        new_object = schema_obj.dump(new_obj).data
        pk = new_object['M_COMPANY_ID']

        master_data_id['M_COMPANY_ID'].append(pk)

        return pk


        #for keys in range(len(master_data.get('company'))):
            #master_data_id[master_data.get('company')[keys]['M_COMPANY_ID']] = []
            #self.post_company_data(keys, master_data.get('company'), master_data_id)

        #for key in range(len(master_data.get('employee'))):
            #self.post_employee_data(key, master_data.get('employee'), master_data_id)

    #def post_company_data(self, json_data, master_data_id):
     #   master_data_id[json_data['M_COMPANY_ID']] = []
      #  changed_generated_id = json_data['M_COMPANY_ID']
       # company_object = Company.query.get(changed_generated_id)
       # company_object = company_schema.dump(company_object).data
        #if not company_object:
         #   company = Company(
          #      NAME=json_data['NAME']
           #     )
            #db.session.add(company)
            #db.session.commit()
            #changed_generated_id = company_schema.dump(company).data
            #master_data_id[json_data['M_COMPANY_ID']].append(changed_generated_id['M_COMPANY_ID'])
        #return master_data_id

   # def post_employee_data(self, keys2, json_data, master_data_id):
    #    changed_generated_id = json_data[keys2]['M_COMPANY_ID']
     #   print(bool(master_data_id.get(changed_generated_id)))
      #  print(master_data_id.keys())
       # if bool(master_data_id.get(changed_generated_id)):
        #    company_id = int("".join(list(map(str, master_data_id.get(changed_generated_id)))))
        #else:
         #   company_id = json_data[keys2]['M_COMPANY_ID']
       # employee_object = Employee.query.get(changed_generated_id)
       # employee_object = employee_schema.dump(employee_object).data

        #if not employee_object:
         #   employee = Employee(
          #      NAME=json_data[keys2]['NAME'],
           #     EMAIL=json_data[keys2]['EMAIL'],
            #    M_COMPANY_ID=company_id
            #)
            #db.session.add(employee)
            #db.session.commit()
        #changed_generated_id = employee_schema.dump(employee).data
        #return changed_generated_id['M_EMPLOYEE_ID']