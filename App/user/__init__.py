from flask import Blueprint

# 不同模块的蓝图不能使用相同的名称,最好使用模块的名称
user_blue = Blueprint('user', __name__,template_folder='templates')

from . import views
