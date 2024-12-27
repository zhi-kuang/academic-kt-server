academic-kt-server
==========================

## 项目结构
```
flask-starter/
├── app
│   ├── controllers
│   ├── data
│   ├── dataset
│   ├── evaluation
│   ├── middlewares
│   ├── router
│   ├── utils
│   └── hooks.py
├── config
├── logs
├── resources
├── model
├── globals.py
├── main.py
└── requirements.txt
```

* `app/hooks.py` - 项目启动前的加载项，都可以在这里执行。
* `config` - 项目配置文件，直接新建 json 文件即可新增配置文件，项目启动时会自动加载。
* `model` - 群体知识追踪模型。
* `globals.py` - 全局变量。
* `main.py` - 项目入口。
* `app/controllers/common/kt.py` - 提供知识追踪模型部署成功后的两个调用接口,/kt/one 和 /kt/class ，分别对应单学生和班级的知识点掌握情况。
* `app/data/` - 包含一些数据处理相关的代码

## 部署
部署前请将 `config/app_conf.json` 中的 `ENV` 的值改为 `"prod"`
