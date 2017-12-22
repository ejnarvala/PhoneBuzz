from flask import Flask, request, render_template, url_for, redirect
from functools import wraps
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.request_validator import RequestValidator


app = Flask(__name__)

def fizzBuzz(number):
	out = []
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
				client = Client()
				lookupNum = client.lookups.phone_numbers(number).fetch()
				print lookupNum.national_format
				success = "Calling " + lookupNum.national_format
		except Exception as ex:
			if(type(ex) is TwilioRestException):
				error = "Invalid Phone Number, Try again"
			else:
				error = str(ex)
	return render_template('index.html', error=error, success=success)



@app.route("/voice", methods=['GET', 'POST'])
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
		except Exception:
			response.say("Invalid Input Entered", voice='alice')
			response.redirect('/voice')
	return str(response)


if __name__ == "__main__":
	app.run(debug=False) 	







