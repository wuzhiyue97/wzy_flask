from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
import pymysql
pymysql.install_as_MySQLdb()
# 0.自定义项目配置类
class Config(object):
    # 开启debug模式
    DEBUG = True
    # mysql 数据库相关配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345678@192.168.171.181:3306/wzy_flask'
    # 关闭数据库修改跟着操作
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    # redis 数据库配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
# 1.创建app对象
app = Flask(__name__)
app.config.from_object(Config)
# 2.创建mysql数据库对象
db = SQLAlchemy(app)
# 3.创建redis数据库对象
# decode_response =True : 能将bytes类型数据转换成字符串
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)
# 4.添加CSRF验证
# 提取cookie中的csrf_token的值
# 提起form表单或者ajax请求头中携带的csrf_token值
# 自动对比这俩个值是否一致
CSRFProtect(app)
@app.route('/index')
def index():
    return 'index'
if __name__ == '__main__':

    app.run(debug=True)