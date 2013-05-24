from flask import Flask

app = Flask(__name__)
app.config.from_object('digitalswitchboard.config')

# Twilio

twilio = TwilioRestClient()

# Blueprints

from digitalswitchboard.views import *
app.register_blueprint(call.mod, url_prefix='/call')
