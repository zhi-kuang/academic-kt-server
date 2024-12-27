import os
import importlib
from app.router.routes import BLUEPRINT_LIST


def register_blueprint(app):
    """
    注册蓝图
    :param app: flask app
    """
    for bp in BLUEPRINT_LIST:
        app.register_blueprint(blueprint=bp['obj'], url_prefix=bp['url_prefix'])


def register_routes(bp_list):
    """
    注册路由
    """
    for bp in bp_list:
        # 动态import路由
        route_dir = os.path.join(os.getcwd(), 'app/controllers', bp['name'])
        for route_file in os.listdir(route_dir):
            filename, ext = os.path.splitext(route_file)
            if ext == '.py' and filename not in ['__init__', '__blueprint__']:
                importlib.import_module('app.controllers.%s.%s' % (bp['name'], filename))


register_routes(BLUEPRINT_LIST)
