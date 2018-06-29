import requests
import arrow
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/rc_predict_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qcqgafnbwwtqdp:95c7a83b4043b97bdbc3c1c671906ad33c4916af4d96ae9db52df732562ec811@ec2-54-235-196-250.compute-1.amazonaws.com:5432/d3gl3fh4221usg?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
	__tablename__ = "data"
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(10))
	humidity = db.Column(db.Numeric(precision=None, asdecimal=True))
	pressure = db.Column(db.Numeric(precision=None, asdecimal=True))
	temperature = db.Column(db.Numeric(precision=None, asdecimal=True))
	description = db.Column(db.String(255))
	icon = db.Column(db.String(5))
	customers = db.Column(db.Integer, nullable=True)
	timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

	def __init__(self, city, humidity, pressure, temperature, description, icon, customers=None, timestamp=datetime.utcnow()):
		self.city = city
		self.humidity = humidity
		self.pressure = pressure
		self.temperature = temperature
		self.description = description
		self.icon = icon
		self.customers = customers
		self.timestamp = timestamp

@app.route("/", methods=['POST', 'GET'])
def index():
	alert = ''
	alert_style=''
	if request.method == 'POST':
		weather = db.session.query(Data).order_by(Data.id.desc()).first()
		last_update = datetime.utcnow() - weather.timestamp
		last_update_secs = last_update.total_seconds()
		last_update_minutes = int(last_update_secs / 60) % 60
		if last_update_minutes <= 10:
			alert_style='alert alert-danger'
			alert = '10 minute break before another update'
			# return render_template("index.html", arrow=arrow, weather=weather, human_time=human_time, home='active', alert=alert)
		else:
			url = 'https://api.openweathermap.org/data/2.5/weather?id=2964574&appid=7d960e942d466535298aa47e39a03ae2'
		
			r = requests.get(url).json()
			
			city = r['name']
			humidity = r['main']['humidity']
			pressure = r['main']['pressure']
			temperature = r['main']['temp']
			description = r['weather'][0]['description']
			icon = r['weather'][0]['icon']

			data = Data(city, humidity, pressure, temperature, description, icon)
			db.session.add(data)
			db.session.commit()
			alert = 'Update Successful'
			alert_style='alert alert-success'

	weather_count = db.session.query(Data).order_by(Data.id.desc()).count()

	if weather_count > 0:

		weather = db.session.query(Data).order_by(Data.id.desc()).first()
		
		# last_update_hours = int(last_update_secs / 3600)		
		
		human_time = arrow.get(weather.timestamp).humanize()

	else:
		weather = {}
		human_time = ''
	

	return render_template("index.html", arrow=arrow, weather=weather, human_time=human_time, home='active', alert=alert, alert_style=alert_style)

@app.route("/records")
def records():
	data = db.session.query(Data).order_by(Data.id.desc()).all()
	return render_template("records.html", arrow=arrow, data=data, records='active')

if __name__ == '__main__':
	app.debug = True
	app.run()