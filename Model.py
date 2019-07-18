from marshmallow_jsonapi import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Company(db.Model):
    __tablename__ = 'company'
    M_COMPANY_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(150), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='employee_name')

    # def __init__(self, NAME):
    #     self.NAME = NAME
    def __init__(self, **kwargs):
        kwargs.pop('M_COMPANY_ID')
        self.__dict__.update(kwargs)


class CompanySchema(ma.Schema):
    M_COMPANY_ID = fields.Integer()
    NAME = fields.String(required=True)
    #id = fields.Relationship(
     #   self_url="/company/{company_id}",
      #  self_url_kwargs={"company_id": "<id>"},
       # related_url="/email/{company_id}",
   # )

    #class Meta:
        #type_ = "companies"
        #self_url = "/company/{id}"
        #self_url_kwargs = {"id": "<id>"}
        #self_url_many = "/companies/"
        #strict = True


class Employee(db.Model):
    __tablename__ = 'employee'
    M_EMPLOYEE_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(250), nullable=False)
    EMAIL = db.Column(db.String(250), nullable=False)
    M_COMPANY_ID = db.Column(db.Integer, db.ForeignKey('company.M_COMPANY_ID'))

    # def __init__(self, NAME, EMAIL, M_COMPANY_ID):
    #     self.NAME = NAME
    #     self.EMAIL = EMAIL
    #     self.M_COMPANY_ID = M_COMPANY_ID

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class EmployeeSchema(ma.Schema):
    M_EMPLOYEE_ID = fields.Integer()
    NAME = fields.String(required=True)
    EMAIL = fields.String()
    M_COMPANY_ID = fields.Integer()
    #email = fields.Relationship(
        #self_url="/employee/{employee_id}/relationships/employee_id",
        #self_url_kwargs={"employee_id": "<id>"},
        #related_url="/email/{employee_id}",
    #)

    #class Meta:
        #type_ = "employees"
        #self_url = "/employees/{id}"
        #self_url_kwargs = {"id": "<id>"}
        #self_url_many = "/employees/"
        #strict = True


