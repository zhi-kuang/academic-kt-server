from flask_cors import CORS
from globals import global_vals


def register_cors(app):
    app_conf = global_vals['config']['app_conf']
    CORS(app, origins=app_conf['CORS_ORIGINS'])
