import json
import random
import heapq

data_json = {
    "class": 1,     # 班级号
    "averageScore": 0,     # 班级平均分
    "accuracy": 0.0,        # 正确率
    "studentDistribution": {},  # 学生等级分布
    "scoreRangeDistribution": {},  # 学生分数段人数分布
    "atRiskStudents": [],         # 重点关注的k个学生
    "class_knowledge_points": [],  # 班级知识点掌握情况
    "average_overall": 0.0, # 班级知识点总平均掌握概率
    "weak_knowledge_point_topk": [] # 薄弱的k个知识点
}


# 计算班级正确率
def calculate_class_accuracy(file_path):
    total_questions = 0
    correct_answers = 0
    line_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_count += 1
                line = line.strip()

                # 每个学生的数据包含三行
                if line_count % 3 == 1:
                    # 第一行表示题目数量
                    total_questions += int(line)
                elif line_count % 3 == 0:
                    # 第三行表示答题情况，0 表示错，1 表示对
                    answers = line.split(',')
                    correct_answers += sum(1 for answer in answers if answer.strip() == "1")

        # 计算并返回正确率
        accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        return round(accuracy, 2)

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except ValueError:
        print("文件格式错误")
    except Exception as e:
        print(f"发生错误: {e}")


class Student:
    def __init__(self, index, accuracy):
        self.index = index  # 学生序号
        self.accuracy = accuracy  # 正确率


# 重点关注的前k个学生
def find_focus_students(file_path, k=3):
    students = []
    student_index = 1

    try:
        with open(file_path, 'r') as file:
            line_count = 0
            student_total_questions = 0
            student_correct_answers = 0

            for line in file:
                line_count += 1
                line = line.strip()

                if line_count % 3 == 1:
                    # 第一行是题目数量
                    student_total_questions = int(line)
                elif line_count % 3 == 0:
                    # 第三行是答题情况
                    answers = line.split(',')
                    student_correct_answers = sum(1 for answer in answers if answer.strip() == "1")

                    # 计算正确率
                    accuracy = (student_correct_answers / student_total_questions) * 100
                    students.append(Student(student_index, accuracy))

                    student_index += 1

        # 排序，按照正确率从低到高
        students.sort(key=lambda student: student.accuracy)

        # 获取重点关注学生（正确率最低的k个）
        focus_students = students[:k]
        focus_student_ids = [student.index for student in focus_students]

        return focus_student_ids, focus_students

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except ValueError:
        print("文件格式错误")
    except Exception as e:
        print(f"发生错误: {e}")


# 从knowledge_point.json中提取学生对应的知识点掌握情况
def get_knowledge_points(file_path, student_ids):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        student_data = {}
        for student in data['students']:
            if student['student_id'] in student_ids:
                student_info = {
                    "student_id": student['student_id'],
                    "accuracy": student['accuracy'],
                    "score": student['score'],
                    "knowledge_points": student['knowledge_points']
                }
                student_data[student['student_id']] = student_info

        return student_data

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 格式错误")
    except Exception as e:
        print(f"发生错误: {e}")


# 生成包含重点关注学生信息的data.json
def create_atRiskStudents(focus_students, knowledge_points_data):


    for student_id in focus_students:
        if student_id in knowledge_points_data:
            student_info = knowledge_points_data[student_id]
            data_json['atRiskStudents'].append(student_info)

def calculate_student_accuracy(file_path):
    class Student:
        def __init__(self, student_id, accuracy, score):
            self.student_id = student_id  # 学生ID
            self.accuracy = accuracy  # 学生正确率
            self.score = score  # 学生得分  目前和正确率一致

    students = []  # 存储所有学生的正确率

    try:
        with open(file_path, 'r') as file:
            line_count = 0
            student_total_questions = 0
            student_correct_answers = 0
            student_id = 1  # 学生的ID从1开始

            for line in file:
                line_count += 1
                line = line.strip()

                if line_count % 3 == 1:
                    # 第一行表示题目数量
                    student_total_questions = int(line)
                elif line_count % 3 == 0:
                    # 第三行表示答题情况，0 表示错，1 表示对
                    answers = line.split(',')
                    student_correct_answers = sum(1 for answer in answers if answer.strip() == "1")

                    # 计算该学生的正确率
                    accuracy = (
                                           student_correct_answers / student_total_questions) * 100 if student_total_questions > 0 else 0

                    # 创建学生对象并存储
                    students.append(Student(student_id, str(round(accuracy, 4)) + '%', round(accuracy, 4)))

                    student_id += 1  # 学生ID递增

        # 返回所有学生的正确率
        return students

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except ValueError:
        print("文件格式错误")
    except Exception as e:
        print(f"发生错误: {e}")

def process_knowledge_points(class_file_path, input_file_path, output_file_path):
    students_data = {"students": []}  # 用于存储所有学生的数据
    students_data_info = calculate_student_accuracy(class_file_path)
    try:
        with open(input_file_path, 'r') as file:
            student_id = 1  # 学生 ID 从 1 开始
            for line in file:
                line = line.strip()
                if line:
                    # 处理每一行
                    points = line.replace('[', '').replace(']', '').strip().split(', ')

                    # 构造知识点格式
                    knowledge_points = [{"知识点" + str(i + 1): point} for i, point in enumerate(points)]

                    # 创建学生的 JSON 数据
                    student_data = {
                        "student_id": student_id,
                        "accuracy": students_data_info[student_id - 1].accuracy,
                        "score": students_data_info[student_id - 1].score,
                        "knowledge_points": knowledge_points
                    }
                    students_data["students"].append(student_data)
                    student_id += 1  # 增加学生 ID

        # 将结果写入 JSON 输出文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(students_data, output_file, ensure_ascii=False, indent=4)

        print(f"处理完成，结果已保存到 {output_file_path}")

    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

def generate_trend_data(current_score):
    trend_data = [f"{current_score:.4f}"]  # 添加当前掌握情况
    for i in range(4):  # 生成接下来的4个数据点
        fluctuation = random.uniform(-0.5, 0.5)  # 随机波动 -0.5 到 0.5 之间
        new_score = max(0.0, min(1.0, float(trend_data[i]) + fluctuation))  # 确保掌握情况在 0 到 1 之间
        trend_data.append(f"{new_score:.4f}")  # 保留四位小数
    return trend_data


def process_knowledge_point_trends(input_file_path, output_file_path):
    students_list = []  # 用于存储所有学生的数据

    try:
        with open(input_file_path, 'r') as file:
            student_id = 1

            for line in file:
                values = line.strip().replace("[", "").replace("]", "").split(",")
                knowledge_points = []

                for i, value in enumerate(values):
                    current_score = float(value.strip())
                    trend_data = generate_trend_data(current_score)

                    point_data = {"Trend": trend_data}
                    knowledge_points.append({f"知识点{i + 1}": point_data})

                student_data = {
                    "student_id": student_id,
                    "knowledge_points": knowledge_points
                }
                students_list.append(student_data)
                student_id += 1  # 增加学生 ID

        # 将结果写入 JSON 输出文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump({"students": students_list}, output_file, ensure_ascii=False, indent=4)

        print(f"处理完成，结果已保存到 {output_file_path}")

    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

def calculate_score_range_distribution(file_path):
    score_range_distribution = {
        "0-60": 0,
        "60-80": 0,
        "80-100": 0
    }

    try:
        with open(file_path, 'r') as file:
            line_count = 0
            student_total_questions = 0
            student_correct_answers = 0

            for line in file:
                line_count += 1

                # 每个学生的数据包含三行
                if line_count % 3 == 1:
                    # 第一行表示题目数量
                    student_total_questions = int(line.strip())
                elif line_count % 3 == 0:
                    # 第三行表示答题情况，0 表示错，1 表示对
                    answers = line.strip().split(",")
                    student_correct_answers = 0
                    for answer in answers:
                        if answer.strip() == "1":
                            student_correct_answers += 1

                    # 计算该学生的正确率
                    accuracy = (student_correct_answers / student_total_questions) * 100

                    # 分配到相应的分数段
                    if accuracy < 60:
                        score_range_distribution["0-60"] += 1
                    elif accuracy < 80:
                        score_range_distribution["60-80"] += 1
                    else:
                        score_range_distribution["80-100"] += 1

        # 输出结果
        print("\"scoreRangeDistribution\": {")
        for range, count in score_range_distribution.items():
            print(f'    "{range}": {count},')
        print("}")

        data_json["scoreRangeDistribution"] = score_range_distribution

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

def calculate_student_grades(file_path):
    student_distribution = {
        "excellent": 0,
        "good": 0,
        "average": 0,
        "poor": 0
    }
    excellent_count = 0
    good_count = 0
    average_count = 0
    poor_count = 0

    try:
        with open(file_path, 'r') as file:
            line_count = 0
            student_total_questions = 0
            student_correct_answers = 0

            for line in file:
                line_count += 1

                # 每个学生的数据包含三行
                if line_count % 3 == 1:
                    # 第一行表示题目数量
                    student_total_questions = int(line.strip())
                elif line_count % 3 == 0:
                    # 第三行表示答题情况，0 表示错，1 表示对
                    answers = line.strip().split(",")
                    student_correct_answers = sum(1 for answer in answers if answer.strip() == "1")

                    # 计算该学生的正确率
                    accuracy = student_correct_answers / student_total_questions

                    # 分类
                    if accuracy >= 0.90:
                        student_distribution["excellent"] += 1
                    elif accuracy >= 0.80:
                        student_distribution["good"] += 1
                    elif accuracy >= 0.60:
                        student_distribution["average"] += 1
                    else:
                        student_distribution["poor"] += 1

        # 输出结果
        print("\"优良中差人数f分布\": {")
        for range, count in student_distribution.items():
            print(f'    "{range}": {count},')
        print("}")
        data_json["studentDistribution"] = student_distribution

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

def calculate_average_knowledge(file_path, k=10):
    class_knowledge_points = []
    try:
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 存储每个知识点的总分与学生数
        knowledge_point_scores = {}

        # 遍历每个学生的数据
        for student in data.get('students', []):
            knowledge_points = student.get('knowledge_points', [])
            for point in knowledge_points:
                for knowledge_point, score_str in point.items():
                    score = float(score_str)  # 转换为浮动数
                    if knowledge_point not in knowledge_point_scores:
                        knowledge_point_scores[knowledge_point] = {'total_score': 0, 'count': 0}
                    knowledge_point_scores[knowledge_point]['total_score'] += score
                    knowledge_point_scores[knowledge_point]['count'] += 1

        # 计算每个知识点的平均掌握情况
        knowledge_point_avg_scores = []
        for knowledge_point, scores in knowledge_point_scores.items():
            avg_score = scores['total_score'] / scores['count']
            knowledge_point_avg_scores.append((knowledge_point, avg_score))
            class_knowledge_points.append({knowledge_point : round(avg_score, 4)})

        # 计算所有知识点的平均掌握情况
        total_score_sum = sum([score for _, score in knowledge_point_avg_scores])
        average_overall = total_score_sum / len(knowledge_point_avg_scores) if knowledge_point_avg_scores else 0

        # 输出所有知识点的平均掌握情况
        print("所有知识点的平均掌握情况：")
        for knowledge_point, avg_score in knowledge_point_avg_scores:
            print(f"{knowledge_point}: {avg_score:.4f}", end=" ")

        data_json["class_knowledge_points"] = class_knowledge_points
        # 找出最薄弱的k个知识点（掌握情况最低的）
        weakest_k_points = heapq.nsmallest(k, knowledge_point_avg_scores, key=lambda x: x[1])
        weak_knowledge_point_topk = []
        # 输出最薄弱的知识点
        print(f"\n最薄弱的 {k} 个知识点：")
        for knowledge_point, avg_score in weakest_k_points:
            print(f"{knowledge_point}: 平均掌握情况 {avg_score:.4f}", end=" ")
            weak_knowledge_point_topk.append({knowledge_point : round(avg_score, 4)})

        data_json["weak_knowledge_point_topk"] = weak_knowledge_point_topk
        # 输出所有知识点的总平均掌握情况
        print(f"\n所有知识点的总平均掌握情况: {average_overall:.4f}")
        data_json["average_overall"] = round(average_overall, 4)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的JSON格式")
    except Exception as e:
        print(f"发生错误: {e}")

def create_data_json():
    # 使用示例
    class_file_path = "app/data/class_problem_sequence.csv"
    input_file_path = "app/data/mastery_knowledge_points.txt"
    output_file_path = "app/data/output/knowledge_point.json"
    output_data_json = "app/data/output/data.json"  # 输出的data.json文件路径
    process_knowledge_points(class_file_path, input_file_path, output_file_path)
    # 计算班级的正确率
    accuracy = calculate_class_accuracy(class_file_path)
    # if accuracy is not None:
    #     print(f"班级的正确率为：{accuracy}%")
    class_id = "1"  # 例如班级1
    data_json["class"] = class_id
    data_json['accuracy'] = accuracy
    data_json['averageScore'] = accuracy

    # data.json 用于班级学情诊断报告

    knowledge_point_file_path = output_file_path  # 知识点掌握情况文件

    # 1. 获取重点关注的学生（准确率最低的k个）
    focus_student_ids, focus_students = find_focus_students(class_file_path, k=3)

    # 2. 获取这些学生的知识点掌握情况
    knowledge_points_data = get_knowledge_points(knowledge_point_file_path, focus_student_ids)

    # 3. 重点关注学生添加到data.json中
    create_atRiskStudents(focus_student_ids, knowledge_points_data)



    # 使用示例
    calculate_score_range_distribution(class_file_path)

    # 使用示例
    calculate_student_grades(class_file_path)

    # 使用示例
    file_path = "app/data/output/knowledge_point.json"
    calculate_average_knowledge(file_path, k=10)

    # 将data.json文件保存起来
    try:
        with open(output_data_json, 'w', encoding='utf-8') as output_data_json:
            json.dump(data_json, output_data_json, ensure_ascii=False, indent=4)
            print(f"已生成 {output_file_path} 文件")
    except Exception as e:
        print(f"保存文件时发生错误: {e}")

    return data_json

def personal_data_json():
    input_file_path = "app/data/mastery_knowledge_points.txt"
    # 用于学生的兴趣变化, 目前还没取的消失的知识点变化情况的中间状态
    output_file_path = "app/data/output/knowledge_point_trends.json"

    process_knowledge_point_trends(input_file_path, output_file_path)

create_data_json()