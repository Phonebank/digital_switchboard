from flask import Flask, send_from_directory
from twilio.rest import TwilioRestClient

app = Flask(__name__)
app.config.from_object('digitalswitchboard.config')

# Twilio

twilio = TwilioRestClient()

# Helpers

def cdn(path):
    return app.config['CDN_BASE'] + path

# Blueprints

from digitalswitchboard.views import *
app.register_blueprint(call.mod, url_prefix='/call')
