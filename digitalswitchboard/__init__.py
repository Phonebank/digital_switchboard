from flask import Flask, send_from_directory

app = Flask(__name__)
app.config.from_object('digitalswitchboard.config')

# Twilio

from twilio.rest import TwilioRestClient
twilio = TwilioRestClient()

# Sunlight Congress

from sunlight import congress

# Helpers

def cdn(path):
    return app.config['CDN_BASE'] + path

# Blueprints

from digitalswitchboard.views import *
app.register_blueprint(call.mod, url_prefix='/call')
