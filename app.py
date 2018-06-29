import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# DATABASE_URL: postgres://qcqgafnbwwtqdp:95c7a83b4043b97bdbc3c1c671906ad33c4916af4d96ae9db52df732562ec811@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d3gl3fh4221usg

app = Flask(__name__)

@app.route("/")
def index():
	url = 'https://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b6907d289e10d714a6e88b30761fae22'
	
	r = requests.get(url).json()
	
	weather = {
		'city' : r['name'],
		'humidity' : r['main']['humidity'],
		'pressure' : r['main']['pressure'],
		'temperature' : r['main']['temp'],
		'description' : r['weather'][0]['description'],
		'icon' : r['weather'][0]['icon'],

	}

	print(weather)

	return render_template("index.html", weather=weather)

@app.route("/records")
def records():
	return render_template("records.html")

if __name__ == '__main__':
	app.debug = True
	app.run()