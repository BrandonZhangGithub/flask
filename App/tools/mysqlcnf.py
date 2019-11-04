#sqlalchemy 有两个版本 flask-sqlalchemy（反向迁移默认不可用）   sqlalchemy
#正向 把代码导入到数据库中，每次迁移都需要把之前的库删除
#反向 把表导入到代码中，自动生成模块，数据依然保留，但是会把模块中的自定义注释删掉

#导入数据库的配置参数
from App.settings import MYSQL

#使用sqlalchemy拼接连接方式
#mysql+pymysql://username:password@host:port/database
def sqlalchemy_database_uri(DBCNF):
    #DBCNF传入的必须是一个字典

    #存储类型
    dialect = DBCNF.get("dialect", 'mysql')
    #引擎
    driver = DBCNF.get("driver", 'pymysql')
    #用户
    username = DBCNF.get("username", 'root')
    #密码
    password = DBCNF.get("pwd", 'root')
    #主机地址
    host = DBCNF.get("host", 'localhost')
    #端口
    port = DBCNF.get("port",'3306')
    #数据库
    database = DBCNF.get("database",'flask')

    return f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}"

#flask中sql配置
class MysqlConfig():
    #链接许可
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #输出sql语句
    SQLALCHEMY_ECHO = True
#flask_sqlalchemy的联结argument，是一个字符串
    SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri(MYSQL)

