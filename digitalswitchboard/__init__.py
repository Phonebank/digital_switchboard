from flask import Flask, send_from_directory
from twilio.rest import TwilioRestClient

app = Flask(__name__)
app.config.from_object('digitalswitchboard.config')

# Twilio

twilio = TwilioRestClient()

# Blueprints

from digitalswitchboard.views import *
app.register_blueprint(call.mod, url_prefix='/call')

@app.route('/static/<filename>')
def static(filename):
    return send_from_directory('static', filename)
