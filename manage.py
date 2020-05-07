from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, redis_store
from info.moduls.models import User
import pymysql
import logging
pymysql.install_as_MySQLdb()

# 调用工厂方法创建app对象
app = create_app('development')
# 6.给项目添加迁移文件
Migrate(app, db)
# 7.创建管理对象
manager = Manager(app)
# 8.根据管理对象添加迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/index')
def index():

    logging.debug("This is a debug log.")
    logging.info("This is a info log.")
    logging.warning("This is a warning log.")
    logging.error("This is a error log.")
    logging.critical("This is a critical log.")

    # flask中也封装了logging模块
    current_app.logger.debug('flask -- debug')
    return 'index'


if __name__ == '__main__':
    # 9.使用管理对象运行项目
    manager.run()
