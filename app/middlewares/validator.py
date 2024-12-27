import traceback
from flask import request, abort
from jsonschema import validate, exceptions
from globals import global_vals


app = global_vals['app']
schema_map = dict()


@app.before_request
def validator():
    """
    请求参数验证中间件
    对不符合规则的请求一律返回 400 Bad Request
    """
    flask_app_conf = global_vals['config']['app_conf']
    method = request.method
    try:
        if method == 'GET':
            _handle_get()
        elif method == 'POST':
            _handle_post()
        else:
            pass
    except exceptions.ValidationError:
        if flask_app_conf['APP_DEBUG_FOR_VALIDATOR']:
            print(traceback.print_exc())
        abort(400)


def register_schema(blueprint_obj, url_rule, schema):
    """
    收集参数验证的 schema，有需要作参数验证的接口都应调用本方法
    此步骤会在服务启动时完成
    :param blueprint_obj: 蓝图对象
    :param url_rule: 需要拦截的url规则
    :param schema: json schema
    """
    schema_map[blueprint_obj.name + url_rule] = schema


def _handle_get():
    params = request.args.to_dict()
    req_schema = schema_map.get(request.base_url.replace(request.root_url, ''), None)
    if req_schema is None:
        return

    validate(instance=params, schema=req_schema)


def _handle_post():
    req_schema = schema_map.get(request.base_url.replace(request.root_url, ''), None)
    if req_schema is None:
        return

    content_type = request.content_type
    if content_type == 'application/json':
        params = request.json
    elif content_type == 'application/x-www-form-urlencoded':
        params = request.form.to_dict()
    else:
        return

    validate(instance=params, schema=req_schema)
