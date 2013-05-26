from flask import Blueprint, request, session
from twilio import twiml
from digitalswitchboard import cdn, congress

mod = Blueprint('call', __name__)

@mod.route('/', methods=['POST'])
def index():
    r = twiml.Response()
    g = r.gather(numDigits=1, action='/call/menu')
    g.play(cdn('/DS1.wav'))
    g.play(cdn('/DS2.wav'))
    g.play(cdn('/DS3.wav'))
    g.play(cdn('/DS4.wav'))
    r.say('I couldn not hear you.', voice='man')
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
            r.say('I did not recognize that option.', voice='man')
            r.redirect()
    else:
        g = r.gather(numDigits=1)
        for i in range(3):
            g.play(cdn('/DS2.wav'))
            g.play(cdn('/DS3.wav'))
            g.play(cdn('/DS4.wav'))
            r.say('I could not hear you. Try again.', voice='man')
        r.say('Goodbye')
    return str(r)

@mod.route('/zipcode', methods=['POST'])
def zipcode():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '9':
            r.redirect('/menu')
        else:
            if len(digits) < 5:
                r.play(cdn('/DS7.wav'))
                r.say(digits, voice='man')
                r.play(cdn('/DS9.wav'))
                r.redirect()
            else:
                r.say('Please wait while we retrieve your representatives')
                r.redirect('/legislators')
    else:
        g = r.gather(numDigits=5)
        for i in range(3):
            g.play(cdn('/DS6.wav'))
            r.say('I could not hear you. Try again.', voice='man')
        r.say('Goodbye')
    return str(r)

@mod.route('/legislators/<string:zipcode>', methods=['POST'])
def legislators(zipcode):
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '9':
            r.redirect('/zipcode')
        else: 
            legislators = session.get('legislators')
            if legislators:
                try:
                    index = int(digits)
                    legislators[digits]
                except TypeError, IndexError:
                    r.say('I did not recognize that option. Try again.', voice='man')
                    r.redirect()
                else:
                    r.say('Dialing')
            else:
                r.redirect()
    else:
        session['legislators'] = congress.legislators_by_zip(zipcode)
        if legislators:
            g = r.gather(numDigits=1)
            for i in range(3):
                for j, l in enumerate(legislators):
                    if j > 9:
                        break
                    name = '%s %s %s' % (l.get('firstname'), l.get('middlename'), l.get('lastname'))
                    title = l.get('title')
                    if title == 'Sen':
                        g.say('Press %s for Senator %s' % (j + 1, name))
                    elif title == 'Rep':
                        g.say('Press %s for Represenative %s' % (j + 1, name))
                    else:
                        g.say('Press %s for %s' % (j + 1, name))
                r.say('I could not hear you. Try again.', voice='man')
            r.say('Goodbye.')
        else:
            r.play(cdn('/DS7.wav'))
            r.say(zipcode, voice='man')
            r.redirect('/zipcode')
    return str(r)
