from flask import Blueprint

mod = Blueprint('call', __name__)

@mod.route('/', methods=['GET'])
def index():
    return 'hello world'
