
from flask import Flask, request
import torch
import os
import json
from app.router.routes import common

from globals import global_vals

app = Flask(__name__)

from app.data.dataloader import getDataLoader
from app.evaluation import eval
from app.utils.data_processing import create_data_json, personal_data_json

URL_RULE = '/kt'

@common.route(URL_RULE + 'Class')
def kg_class():
    # 设置参数
    length = 200
    questions = 124
    bs = 64
    cuda = '0'
    if torch.cuda.is_available():
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    # 加载数据
    testLoader = getDataLoader(bs, questions, length)

    # 定义损失函数
    loss_func = eval.lossFunc(questions, length, device)

    # 测试模型
    pred = eval.test_epoch(global_vals['model'], testLoader, loss_func, device)

    # 存放每个学生的知识掌握情况
    knowledge_state = pred[:, -1, :]

    # 打开文件进行写入
    with open('app/data/mastery_knowledge_points.txt', 'w') as f:
        for i in range(knowledge_state.shape[0]):
            # 对每个元素进行四舍五入，乘以1000再除以1000
            rounded_values = torch.round(knowledge_state[i] * 1000) / 1000
            # 将 rounded_values 转换为列表并写入文件，每行一个列表
            # 也可以使用 Python 的格式化方法来确保输出为 4 位小数
            rounded_values_list = [f"{value:.4f}" for value in rounded_values.tolist()]
            f.write(f"[{', '.join(rounded_values_list)}]\n")

    # 使用列表推导式和字符串格式化来保留 4 位小数
    formatted_values = [[f"{value:.4f}" for value in row] for row in knowledge_state.tolist()]

    # 打印结果
    print(formatted_values)
    print("数据已保存到 'mastery_knowledge_points.txt' 文件")
    data_json = create_data_json()

    return data_json


@common.route(URL_RULE + 'One')
def kg_one():
    student_id = request.args['student_id']
    # 设置参数
    length = 200
    questions = 124
    bs = 64
    cuda = '0'
    if torch.cuda.is_available():
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    # 加载数据
    testLoader = getDataLoader(bs, questions, length)

    # 定义损失函数
    loss_func = eval.lossFunc(questions, length, device)

    # 测试模型
    pred = eval.test_epoch(global_vals['model'], testLoader, loss_func, device)

    # 存放每个学生的知识掌握情况
    knowledge_state = pred[:, -1, :]

    # 打开文件进行写入
    with open('app/data/mastery_knowledge_points.txt', 'w') as f:
        for i in range(knowledge_state.shape[0]):
            # 对每个元素进行四舍五入，乘以1000再除以1000
            rounded_values = torch.round(knowledge_state[i] * 1000) / 1000
            # 将 rounded_values 转换为列表并写入文件，每行一个列表
            # 也可以使用 Python 的格式化方法来确保输出为 4 位小数
            rounded_values_list = [f"{value:.4f}" for value in rounded_values.tolist()]
            f.write(f"[{', '.join(rounded_values_list)}]\n")

    # 使用列表推导式和字符串格式化来保留 4 位小数
    formatted_values = [[f"{value:.4f}" for value in row] for row in knowledge_state.tolist()]

    # 打印结果
    print(formatted_values)
    print("数据已保存到 'mastery_knowledge_points.txt' 文件")
    personal_data_json()
    # 读取JSON文件
    with open("app/data/output/knowledge_point_trends.json", 'r', encoding='utf-8') as file:
        knowledge_point_trends = json.load(file)

    def get_knowledge_points_trends(student_id):
        # 遍历所有学生，查找匹配的 student_id
        for student in knowledge_point_trends['students']:
            if student['student_id'] == student_id:
                return student['knowledge_points']
        return None  # 如果没有找到该学生ID，返回 None

    knowledge_point_trends = get_knowledge_points_trends(int(student_id))
    knowledge_point = '''
    {
      "students": [
        {
          "student_id": 1,
          "accuracy": "60.0%",
          "score": 60.0,
          "knowledge_points": [
            {"知识点1": "0.5680"},
            {"知识点2": "0.2850"},
            {"知识点3": "0.5640"},
            {"知识点4": "0.4090"}
          ]
        },
        {
          "student_id": 2,
          "accuracy": "75.0%",
          "score": 75.0,
          "knowledge_points": [
            {"知识点1": "0.8780"},
            {"知识点2": "0.3450"},
            {"知识点3": "0.7120"},
            {"知识点4": "0.5600"}
          ]
        }
      ]
    }
    '''
    with open("app/data/output/knowledge_point.json", 'r', encoding='utf-8') as file:
        knowledge_point = json.load(file)


    def get_knowledge_points(student_id):
        # 遍历所有学生，查找匹配的 student_id
        for student in knowledge_point['students']:
            if student['student_id'] == student_id:
                return student['knowledge_points']
        return None  # 如果没有找到该学生ID，返回 None

    knowledge_points = get_knowledge_points(int(student_id))
    data = {
        "student_id": student_id ,
        "knowledge_points": knowledge_points,
        "knowledge_point_trends": knowledge_point_trends}
    return data