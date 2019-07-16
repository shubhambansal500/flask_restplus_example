from marshmallow_jsonapi import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='employee_name')

    def __init__(self, name):
        self.name = name


class CompanySchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __init__(self, name, email, company_id):
        self.name = name
        self.email = email
        self.company_id = company_id


class EmployeeSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    email = fields.String()
    company_id = fields.Integer()
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


