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
    r.play(cdn('/DS43.wav'))
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
            r.redirect('/call/info')
        elif digits == '9':
            r.redirect()
        else:
            r.play(cdn('/DS40.wav'))
            r.redirect()
    else:
        for i in range(3):
            g = r.gather(numDigits=1)
            g.play(cdn('/DS2.wav'))
            g.play(cdn('/DS3.wav'))
            g.play(cdn('/DS4.wav'))
            r.play(cdn('/DS43.wav'))
        r.play(cdn('/DS39.wav'))
    return str(r)

@mod.route('/info', methods=['POST'])
def info():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        r.redirect('/call/menu')
    else:
        g = r.gather(numDigits=1)
        g.play(cdn('/DS5.wav'))
        r.redirect('/call/menu')
    return str(r)

@mod.route('/zipcode', methods=['POST'])
def zipcode():
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '9':
            r.redirect('/call/menu')
        else:
            if len(digits) < 5:
                r.play(cdn('/DS7.wav'))
                for digit in ' '.join(digits).split():
                    r.play(cdn('DS%d.wav' % (int(digit) + 44)))
                r.play(cdn('/DS9.wav'))
                r.redirect()
            else:
                r.play(cdn('/DS41.wav'))
                r.redirect('/call/legislators/%s' % digits)
    else:
        for i in range(3):
            g = r.gather(numDigits=5)
            g.play(cdn('/DS6.wav'))
            r.play(cdn('/DS43.wav'))
        r.play(cdn('/DS39.wav'))
    return str(r)

@mod.route('/legislators/<string:zipcode>', methods=['POST'])
def legislators(zipcode):
    r = twiml.Response()
    digits = request.form.get('Digits')
    if digits:
        if digits == '9':
            r.redirect('/call/zipcode')
        else: 
            legislators = session.get('legislators')
            if legislators:
                try:
                    index = int(digits) - 1
                    l = legislators[index]
                except (TypeError, IndexError):
                    r.play(cdn('/DS40.wav'))
                    r.redirect()
                else:
                    name = re.sub(' +', ' ', '%s %s %s' % (l.get('firstname'), l.get('middlename'), l.get('lastname')))
                    legislator_phone = l.get('phone')
                    if legislator_phone:
                        r.play(cdn('/DS44.wav'))
                        r.dial(legislator_phone)
                    else:
                        r.play(cdn('/DS42.wav'))
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
                        g.play(cdn('/DS%d.wav' % (j + 20)))
                        g.say(name)
                    elif title == 'Rep':
                        g.play(cdn('/DS%d.wav' % (j + 30)))
                        g.say(name)
                r.play(cdn('/DS43.wav'))
            r.play(cdn('/DS39.wav'))
        else:
            r.play(cdn('/DS7.wav'))
            for digit in ' '.join(zipcode).split():
                r.play(cdn('DS%d.wav' % (int(digit) + 44)))
            r.redirect('/call/zipcode')
    return str(r)
