from flask import Flask
from twilio.twiml.voice_response import VoiceResponse


app = Flask(__name__)

@app.route("/", methods=['Get', 'POST'])
def phone_buzz():
	message = "Welcome to Ejnar's Phone Buzz, Please Enter a Number"
	response = VoiceResponse()
	response.say(message)

	return str(response)


if __name__ == "__main__":
	app.run(debug=True) 	