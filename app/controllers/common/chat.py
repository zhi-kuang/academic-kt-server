import json
import uuid
import time
from flask import request
from app.router.routes import common
from app.middlewares.validator import register_schema
from globals import global_vals


URL_RULE = '/chatglm'
PARAMS_SCHEMA = {
    'type': 'object',
    'required': ['key', 'prompts'],
    'properties': {
        'key': {'type': 'string'},
        'prompts': {'type': 'string'},
    },
}
register_schema(common, URL_RULE, PARAMS_SCHEMA)


@common.route(URL_RULE, methods=['POST'])
def chat():
    app = global_vals['app']
    session_cache = global_vals['session_cache']
    params = request.json
    key = str(params['key'])
    prompts = str(params['prompts'])

    if key in session_cache.keys():
        session_cache[key]['modify_timestamp'] = int(time.time())
    else:
        key = str(uuid.uuid4())
        session_cache[key] = {
            'create_timestamp': int(time.time()),
            'modify_timestamp': int(time.time()),
            'history': [],
        }

    response, history = global_vals['model'].chat(global_vals['tokenizer'], prompts, history=session_cache[key]['history'])
    session_cache[key]['history'] = history

    app.logger.info('[%s]-[Q]-%s-[A]-%s' % (key, prompts, response))

    return json.dumps({
        'key': key,
        'response': response,
    }, ensure_ascii=False)
