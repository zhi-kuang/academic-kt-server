FROM python:3.10-slim

#将此目录设为工作目录
WORKDIR /academic-kt-server

#将该目录下的所有文件拷贝到镜像容器中
COPY . /academic-kt-server

#安装项目依赖  
RUN pip install --no-cache-dir -r requirements.txt

#node项目启动命令
CMD ["python", "main.py"]