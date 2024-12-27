from flask import Flask
from app.router.routes import common
app = Flask(__name__)


@common.route('/hello')
def hello_world():  # put application's code here

    return 'Hello World!'