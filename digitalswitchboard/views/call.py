from flask import Blueprint, request
from twilio import twiml

mod = Blueprint('call', __name__)

@mod.route('/', methods=['POST'])
def index():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '1':
            r.redirect('/call/zipcode')
        elif digits == '2':
            r.play('/static/DS5.mp3')
            r.redirect()
        else:
            r.say('Sorry, I did not recognize that option.')
    else:
        g = r.gather(numDigits=1)
        g.play('/static/DS1.mp3')
        g.play('/static/DS2.mp3')
        g.play('/static/DS3.mp3')
        g.play('/static/DS4.mp3')
    return str(r)

@mod.route('/zipcode', methods=['POST'])
def zipcode():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if len(digits) < 5:
            r.play('/static/DS7.mp3')
            r.say(digits, voice='man')
            r.play('/static/DS9.mp3')
            r.redirect()
        else:
            r.redirect(settings.SUNLIGHT_URL_ZIPCODE % digits)
    else:
        g = r.gather(numDigits=5)
        g.play('/static/DS6.mp3')
    return str(r)

@mod.route('/zipcode-callback', methods=['POST'])
def zipcode_callback():
    r = twiml.Response()
    r.say('Done')
    return str(r)
