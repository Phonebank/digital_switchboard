from flask import Blueprint, request, url_for
from twilio import twiml

mod = Blueprint('call', __name__)

SUNLIGHT_ZIPCODE = 'http://calloncongress.sunlightfoundation.com/voice/voting/call/?language=en&zipcode=%s&next_url=https://digital-switchboard.herokuapp.com/call/zipcode-callback'

@mod.route('/', methods=['POST'])
def index():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '1':
            r.redirect('/call/zipcode')
        elif digits == '2':
            r.play(url_for('static', 'DS5.wav'))
            r.redirect()
        else:
            r.say('Sorry, I did not recognize that option.')
    else:
        g = r.gather(numDigits=1)
        g.play(url_for('static', 'DS1.wav'))
        g.play(url_for('static', 'DS2.wav'))
        g.play(url_for('static', 'DS3.wav'))
        g.play(url_for('static', 'DS4.wav'))
    return str(r)

@mod.route('/zipcode', methods=['POST'])
def zipcode():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if len(digits) < 5:
            r.play(url_for('static', 'DS7.wav'))
            r.say(digits, voice='man')
            r.play(url_for('static', 'DS9.wav'))
            r.redirect()
        else:
            r.redirect(settings.SUNLIGHT_ZIPCODE % digits)
    else:
        g = r.gather(numDigits=5)
        g.play(url_for('static', 'DS6.wav'))
    return str(r)

@mod.route('/zipcode-callback', methods=['POST'])
def zipcode_callback():
    r = twiml.Response()
    r.say('Done')
    return str(r)
