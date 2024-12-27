import os
import json
from globals import global_vals


def load_config():
    """
    加载配置
    添加新的配置文件，无需手动配置，
    """
    route_dir = os.path.join(os.getcwd(), 'config')
    for route_file in os.listdir(route_dir):
        filename, ext = os.path.splitext(route_file)
        if ext == '.json':
            with open(os.path.join(route_dir, route_file), 'r') as f:
                global_vals['config'][filename] = json.load(f)
