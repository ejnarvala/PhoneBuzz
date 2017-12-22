# PhoneBuzz
A simple telephone FizzBuzz application

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 2.7 (>=2.7.6)
* (Recommended) virtualenv 

### Installing
Download or Clone and navigate to the directory
```
git clone https://github.com/ejnarvala/PhoneBuzz.git
cd PhoneBuzz/
```


(Optional) Create virtualenv and activate

```
virtualenv [env name]
source [env name]/bin/activate
```


install packages in requirements.txt
```
pip install -r requirements.txt
```

open run.py and fill in TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, endpoint_url, and from_phone_number with values from your twilio account

(OPTIONAL) Place token and sid as environment variables if you do not want them in run.py
```
export TWILIO_AUTH_TOKEN=[your auth token]
```



## Running

Run locally
```
python run.py
```

## Deployment

To deploy on Heroku, just create a new application, then set the endpoint_url in run.py to the link of the app.

From the Heroku CLI, login and add remote
```
heroku login
git init
heroku git:remote -a PhoneBuzz
git add .
git commit -m "deployment"
git push heroku master

```
To set up environment variables, you can access your app's settings through heroku and set them.

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Twilio](https://www.twilio.com/) - API for phone interactions
* [Heroku](https://www.heroku.com/) - Used to deploy to the web

