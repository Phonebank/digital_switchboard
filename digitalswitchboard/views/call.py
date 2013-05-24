from flask import Blueprint
from twilio import twiml

mod = Blueprint('call', __name__)

@mod.route('/', methods=['GET'])
def index():
    r = twiml.Response()
    r.say('Hello world')
    return str(r)
