from flask import Blueprint

order_blue = Blueprint('order', __name__, template_folder='templates', static_folder='static', static_url_path='/s')

from . import views
