import re
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
        for i in range(3):
            g = r.gather(numDigits=1)
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
                r.redirect('/call/legislators/%s' % digits)
    else:
        for i in range(3):
            g = r.gather(numDigits=5)
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
                    index = int(digits) - 1
                    name = re.sub(' +', ' ', '%s %s %s' % (l.get('firstname'), l.get('middlename'), l.get('lastname')))
                    legislator = legislators[index]
                except TypeError, IndexError:
                    r.say('I did not recognize that option. Try again.', voice='man')
                    r.redirect()
                else:
                    legislator_phone = legislator.get('phone')
                    if legislator_phone:
                        r.say('Dialing %s' % name)
                        r.dial(legislator_phone)
                    else:
                        r.say('This legislator does not have a phone number on file.')
            else:
                r.redirect()
    else:
        session['legislators'] = congress.legislators_for_zip(zipcode)
        if session['legislators']:
            for i in range(3):
                g = r.gather(numDigits=1)
                for j, l in enumerate(session['legislators']):
                    if j > 9:
                        break
                    name = re.sub(' +', ' ', '%s %s %s' % (l.get('firstname'), l.get('middlename'), l.get('lastname')))
                    title = l.get('title')
                    if title == 'Sen':
                        g.say('Press %s to call Senator %s' % (j + 1, name))
                    elif title == 'Rep':
                        g.say('Press %s to call Represenative %s' % (j + 1, name))
                    else:
                        g.say('Press %s to call %s' % (j + 1, name))
                r.say('I could not hear you. Try again.', voice='man')
            r.say('Goodbye.')
        else:
            r.play(cdn('/DS7.wav'))
            r.say(zipcode, voice='man')
            r.redirect('/zipcode')
    return str(r)
