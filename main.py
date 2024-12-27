from gevent import pywsgi
from globals import global_vals
from config import load_config
from app.hooks import run_hooks
from app.middlewares.cors import register_cors
from app.router import register_blueprint
from app.middlewares import register_middlewares
from app.utils.logger import create_logger

if __name__ == '__main__':
    # 加载配置
    load_config()

    # global values
    flask_app_conf = global_vals['config']['app_conf']
    app = global_vals['app']

    # 创建 logger
    create_logger(app)
    # 跨域
    register_cors(app)
    # 注册蓝图
    register_blueprint(app)
    # 注册中间件
    register_middlewares(app)

    # 运行项目启动前加载项
    run_hooks()

    if flask_app_conf['ENV'] == 'dev':
        app.run(debug=flask_app_conf['APP_DEBUG'], host=flask_app_conf['HTTP_HOST'], port=flask_app_conf['HTTP_PORT'])
    elif flask_app_conf['ENV'] == 'prod':
        server = pywsgi.WSGIServer((flask_app_conf['HTTP_HOST'], flask_app_conf['HTTP_PORT']), app)
        server.serve_forever()
