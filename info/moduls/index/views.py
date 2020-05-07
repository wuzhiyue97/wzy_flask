from info.moduls.index import index_bp
from info import redis_store
# 3.使用蓝图对象装饰视图函数
@ index_bp.route('/')
def index():
    redis_store.setex('name',30,'laowang')
    return 'index'