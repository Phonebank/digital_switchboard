from flask import Blueprint, request
from twilio import twiml
from digitalswitchboard import cdn

mod = Blueprint('call', __name__)

SUNLIGHT_ZIPCODE = 'http://calloncongress.sunlightfoundation.com/voice/voting/call/?language=en&zipcode=%s&next_url=https://digital-switchboard.herokuapp.com/call/zipcode-callback'

@mod.route('/', methods=['POST'])
def index():
    r = twiml.Response()
    g = r.gather(numDigits=1, action='/call/menu')
    g.play(cdn('/DS1.wav'))
    r.redirect('/call/menu')
    return str(r)

@mod.route('/menu', methods=['POST'])
def menu():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '1':
            r.redirect('/call/zipcode')
        elif digits == '2':
            r.play(cdn('/DS5.wav'))
            r.redirect()
        else:
            r.say('Sorry, I did not recognize that option.', voice='man')
    else:
        g = r.gather(numDigits=1)
        for i in range(3):
            g.play(cdn('/DS2.wav'))
            g.play(cdn('/DS3.wav'))
            g.play(cdn('/DS4.wav'))
        r.say('Goodbye')
    return str(r)

@mod.route('/zipcode', methods=['POST'])
def zipcode():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if len(digits) < 5:
            r.play(cdn('/DS7.wav'))
            r.say(digits, voice='man')
            r.play(cdn('/DS9.wav'))
            r.redirect()
        else:
            r.redirect(SUNLIGHT_ZIPCODE % digits)
    else:
        g = r.gather(numDigits=5)
        for i in range(3):
            g.play(cdn('/DS6.wav'))
        r.say('Goodbye')
    return str(r)

@mod.route('/zipcode-callback', methods=['POST'])
def zipcode_callback():
    r = twiml.Response()
    r.say('Done')
    return str(r)
