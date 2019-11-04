from App import create_app
from flask_script import Manager
from App.user import user_blue
from App.order import order_blue

app = create_app()

# 从配置对象中进行读取
# class DefaultConfig(object):
#     SECRET_KEY = '123456ASDFG'
#
#
# app.config.from_object(DefaultConfig)


# 从配置文件中进行读取  settings.py
# app.config.from_pyfile('settings.py')

# 从环境变量中读取
# Linux的环境 export  SETTING='settings.py'  echo $SETTING
# app.config.from_envvar('SETTING')


# @app.route('/')
# def index():
#     # return '<img src="/s/imgs/1.jpg" />'
#     # render_template会自动寻找template_filder中的路径 /template/index.html
#     # render_template会把html中的所有编码当作是字符串
#
#     # path = '/s/imgs/1.jpg'
#     # return render_template('index.html', path=path)
#
#     # 获取flask中的配置
#     return 123

# 注册蓝图
app.register_blueprint(user_blue, url_prefix='/u')
app.register_blueprint(order_blue, url_prefix='/o')

# runserver  -rd
manager = Manager(app=app)
if __name__ == '__main__':
    manager.run()