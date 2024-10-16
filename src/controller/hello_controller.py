from flask import Blueprint

bp = Blueprint('hello_controller', __name__)

@bp.route('/hello')
def index():
    return "Hello from hello_controller!"
