from flask import Flask
from apis import api
from Model import db
import logging

#logging_employee_api()
app = Flask(__name__)
app.config.from_object('config')
api.init_app(app)
db.init_app(app)


def logging_employee_api():
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app.run(debug=True)