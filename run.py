from flask import Flask, request, render_template, url_for, redirect, abort
from functools import wraps
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.request_validator import RequestValidator
import os, sys


################################
#Place your Twilio token/sid here if you have not
#exported them to the environment
TWILIO_AUTH_TOKEN = ''
TWILIO_ACCOUNT_SID = ''
#Url for making calls from app
endpoint_url = 'https://phonebuzz-lendup.herokuapp.com/voice'
################################

if not (len(TWILIO_ACCOUNT_SID) == 0 or len(TWILIO_AUTH_TOKEN) == 0):
	print "Environment Variables Updated"
	os.environ['TWILIO_AUTH_TOKEN'] = TWILIO_AUTH_TOKEN
	os.environ['TWILIO_ACCOUNT_SID'] = TWILIO_ACCOUNT_SID
elif (os.environ.get('TWILIO_ACCOUNT_SID') == None) or (os.environ.get("TWILIO_AUTH_TOKEN") == None):
	print "No environment Variables set!"
	sys.exit()
else:
	print "Using Pre-set Configurations"





app = Flask(__name__)

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function
def fizzBuzz(number):
	out = []
	if(number == 0):
		raise ValueError()
	else:
		for i in range(1,number+1):
			toAppend = ''
			if(i % 3 == 0):
				toAppend += 'Fizz'
			if(i % 5 == 0):
				toAppend += 'Buzz'
			if(len(toAppend) == 0):
				out.append(i)
			else:
				out.append(toAppend)
	return out







@app.route("/", methods=['GET','POST'])
def index():
	error = None
	success = None
	if request.method == 'POST':
		try:
			number = request.form['phonenumber']
			client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get("TWILIO_AUTH_TOKEN"))
			lookupNum = client.lookups.phone_numbers(number).fetch()
			call = client.calls.create(to=lookupNum.phone_number, from_="+14074104685",url=endpoint_url)
			success = "Called " + lookupNum.national_format
			print call.sid
		except Exception as ex:
			print ex
			if(type(ex) is TwilioRestException):
				error = "Invalid Phone Number, Try again"
			else:
				error = str(ex)
	return render_template('index.html', error=error, success=success)


@app.route("/voice", methods=['GET', 'POST'])
@validate_twilio_request
def phone_buzz():
	response = VoiceResponse()
	gather = Gather(action='/process_gather')
	response.say("Welcome to Phone Buzz", voice='alice')
	response.pause(1)
	gather.say("Please Enter a number and press pound to submit", voice='alice')
	response.append(gather)
	response.redirect('/voice')
	return str(response)


@app.route("/process_gather", methods=['GET', 'POST'])
@validate_twilio_request
def process_gather():
	response = VoiceResponse()
	if 'Digits' in request.values:
		inputString = request.values['Digits']
		print 'input String = ' + inputString
		try:
			inputNum = int(inputString)
			fbArr = fizzBuzz(inputNum)
			for i in fbArr:
				response.say(str(i), voice='alice')
		except ValueError:
			response.say("Invalid Input Entered", voice='alice')
			response.redirect('/voice')
	return str(response)


if __name__ == "__main__":
	app.run() 	







