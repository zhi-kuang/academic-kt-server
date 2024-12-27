from flask import request
from globals import global_vals


app = global_vals['app']


@app.before_request
def dev():
    """
    此中间件是为了解决在 flask 开发服务器中的某些 bug
    详见 flask 的 issue#4507
    """
    data = request.data
