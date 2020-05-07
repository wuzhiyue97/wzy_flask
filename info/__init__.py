# 业务文件夹

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler

# 当app对象不存在的时候,并没有真正做数据库初始化操作
db = SQLAlchemy()
# redis数据库对象
redis_store = None  # type:StrictRedis


def write_log(config_class):
    # 记录日志信息

    # 设置日志的记录等级
    logging.basicConfig(level=config_class.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小100M、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 将app的创建封装到:工厂方法中
# config_name = development&production
def create_app(config_name):
    # 1.创建app对象
    app = Flask(__name__)
    # 获取项目配置类
    # config_dict['development'] -->DevelopmentConfig -- 开发模式下的app对象
    # config_dict['production'] -->ProductionConfig -- 开发模式下的app对象
    config_class = config_dict[config_name]
    app.config.from_object(config_class)
    # 记录日志
    write_log(config_class)

    # 2.创建mysql数据库对象,懒加载,延迟初始化,当app存在的啥情况,才做真实的数据库初始化操作
    db.init_app(app)
    # 3.创建redis数据库对象
    # decode_response =True : 能将bytes类型数据转换成字符串
    # redis_store.set('key','value')  -->数据保存到0号数据库
    # 懒加载
    global redis_store
    redis_store = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)
    # 4.添加CSRF验证
    # 提取cookie中的csrf_token的值
    # 提起form表单或者ajax请求头中携带的csrf_token值
    # 自动对比这俩个值是否一致
    CSRFProtect(app)
    # 5.将flask.session的存储位置从服务器'内存'调整到'redis'数据库
    Session(app)
    return app
