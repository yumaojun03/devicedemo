# devicedemo

一个基于Openstack规范开发的API Demo

### API 设计规范和文档

  此项目的API设计规范请参考: [API设计规范](/doc/api_design/specification.md)
  
  此项目的API文档生产工具使用请参考: [Swagger简介](/doc/api_design/swagger_usage.md)

### 项目结构

```
.
├── AUTHORS      
├── ChangeLog    
├── devicedemo  
│   ├── api　　　　   
│   │   ├── app.py      
│   │   ├── config.py
│   │   ├── controllers
│   │   │   ├── __init__.py
│   │   │   ├── root.py
│   │   │   └── v1
│   │   │       ├── controller.py
│   │   │       ├── devices.py
│   │   │       └── __init__.py
│   │   ├── expose.py
│   │   ├── hooks.py
│   │   └── __init__.py
│   ├── cmd
│   │   ├── api.py
│   │   └── __init__.py
│   ├── db
│   │   ├── api.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── sqlalchemy
│   │       ├── alembic
│   │       │   ├── env.py
│   │       │   ├── README
│   │       │   ├── script.py.mako
│   │       │   └── versions
│   │       │       ├── e7f6a2fc5d53_create_device_table.py
│   │       │       └── ff7b0e8f7372_create_user_table.py
│   │       └── alembic.ini
│   └── __init__.py
├── devicedemo.db
├── doc
│   └── your_doc_file.md
├── etc
│   └── devicedemo
│       └── your_app.conf
├── LICENSE
├── README.md
├── requirement.txt
├── setup.cfg
├── setup.py
├── test_requirements.txt
└── tools
    └── your_bash_tools.sh
```

1. 项目打包相关文件

    AUTHORS：　 描述项目参与者大
    
    ChangeLog：  描述版本的ChangLog
    
    requirement.txt： 实现自动依赖安装
    
    setup.cfg：　setuptools打包时提供包的元数据
    
    setup.py:    setup命令运行接口

2. 项目配置文件目录

    etc/devicedemo：　devicedemo项目需要的配置文件

3. 项目说明文档目录

    doc/install:  项目安装说明文档
    
    doc/source:   项目产品说明文档

4. 项目源码目录

    + api
    
    > 提高API服务的目录, 整体框架采用OpenStack新项目, 比如Ceilometer和magnum采用的框架
    > 该框架基于对象分发方式进行路由, 是一个轻量级框架, 通过WSME进行请求参数的响应的类型检查
    > 通过Paste + PasteDeploy 完成 WSGI管理, 而关于WSGI应用的部署, 需要参考Pecan官方文档
    > 其中
    > app.py 一般包含了Pecan应用的入口，包含应用初始化代码
    > config.py 包含Pecan的应用配置，会被app.py使用
    > controllers/ 这个目录会包含所有的控制器，也就是API具体逻辑的地方
    > controllers/root.py 这个包含根路径对应的控制器
    > controllers/v1/ 这个目录对应v1版本的API的控制器。如果有多个版本的API，你一般能看到v2等目录
    
    + db
    
    > 提高数据层面API, 使用使用sqlarchemy 作为ORM系统，　基于Alembic进行数据库版本管理
    > 其中
    > api.py 实现一个Connection类，这个类封装了所有的数据库操作接口。我们会在这个类中实现对表的CRUD等操作
    > models.py　定义了所有的模型
    > sqlalchemy/alembic 基于Alembic的配置以及数据信息都存放在此目录中
    
    + cmd
    
    > service需要有一个命令行的管理接口, 这个是实现的用于管理API Service的一个命令行工具
    
5. 单元测试与覆盖率测试(比较复杂Demo未实现)

    在OpenStack的项目中, 这部分很全面复杂, 涉及到如下内容：
    
	测试环境管理: tox
	
	测试用例的运行和管理: testrepository, subunit, coverage
	
	测试用例的编写: unittest, mock, testtools, fixtures, testscena
	
6. 使用virtualenv管理项目的Python环境
    
    为了使得项目保持一个独立干净的Python环境，项目请使用Virtualenv管理环境
    
    比如使用如下命令在项目根目录下为这个项目初始化一个.venv的Python环境`virtualenv --no-site-packages .venv`


### 使用组件参考文档
1. Pecan

    中文文档较少, 这里是[官方文档](http://pecan.readthedocs.io/en/latest/)
    
    这里有一份基于Ceilometer的介绍,涉及对Pecan介绍[Ceilometer API调用流程分析](http://blog.csdn.net/s1234567_89/article/details/51890459)

2. WSME

    文档很少, 这里是[官方文档](https://pythonhosted.org/WSME/)

3. sqlarchemy

    文档很多

4. Alembic

     [基本使用1](http://blog.csdn.net/oranyujian/article/details/48464365)
     
     [基本使用2](http://www.codeweblog.com/%E4%BD%BF%E7%94%A8alembic/)
     
     [官网](http://www.alembic.io/)
    

### 源码安装

  基于本地环境直接部署请查看[源码安装](doc/install/install_from_source.md)

### 基于Docker的安装

  基于Docker容器来部署请查看[Docker安装](doc/install/install_from_huge_docker.md)