from flask import Flask

global_vals = {
    # flask app
    'app': Flask(__name__),
    # 全局配置
    'config': {},

    # 会话缓存
    'session_cache': {},
    # tokenizer
    'tokenizer': None,
    # model
    'model': None,
}
