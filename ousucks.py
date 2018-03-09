import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime as dt
import json
import urllib2

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
    return get_time_intent()

@ask.intent("GetTimeIntent")
def get_time_intent():
    # Unfortunately, Alexa can't get user location
    # Use CST
    speechString=''
    try:
        j = json.load(urllib2.urlopen("http://api.timezonedb.com/v2/get-time-zone?key=G5TI0CSAKHH2&format=json&by=zone&zone=America/Chicago"))
        # Convert to AM/PM
        t = dt.datetime.strptime(j['formatted'].split()[1], "%H:%M:%S")
        ts = t.strftime("%I:%M %p")
        speechString = "It's " + ts + ". . . and OU still sucks!"
    except:
        speechString = "There was a problem reaching the time server"
    speechString.encode('ascii', 'ignore')
    return statement(speechString).simple_card(title='OU Sucks!', content=speechString)

@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)

