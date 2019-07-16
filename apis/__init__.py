from flask_restplus import Api

from .Employees import ns as ns1
from .Hello import ns as ns2
from .Company import ns as ns3
from .Tables import ns as ns4

api = Api(title='Employee table', version='1.0', description='Employees API')

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
