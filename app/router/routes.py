from flask import Blueprint


common = Blueprint(name='common', import_name=__name__)


BLUEPRINT_LIST = [
    {'obj': common, 'name': 'common', 'url_prefix': '/'},
]
