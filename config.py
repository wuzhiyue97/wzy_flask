# 0.自定义项目配置类
from redis import StrictRedis
import logging

class Config(object):
    # 开启debug模式
    DEBUG = True
    # mysql 数据库相关配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345678@192.168.171.181:3306/wzy_flask'
    # 关闭数据库修改跟着操作
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis 数据库配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 配置秘钥
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
    # 将session调整到redis数据库保存的配置信息
    SESSION_TYPE = 'redis'
    # 具体保存到哪个数据库,redis数据库对象
    # redis_store.set('key','value')  -->数据保存到1号数据库
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)
    # 对应session_id需要加密处理
    SESSION_USE_SIGNER = True
    # 不需要永久存储
    SESSION_PERMANENT = False
    # 设置有效存储时间24小时,单位s
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """开发模式配置信息"""
    DEBUG = True

    # 设置成debug级别
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """线上模式配置信息"""
    DEBUG = False

    # 设置成日志级别
    LOG_LEVEL = logging.WARNING

# 提供一个接口给外界调用
config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
