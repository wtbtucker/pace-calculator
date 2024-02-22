from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stanjfsabfltsg:0372cf3be7d1ca33afaf6076e4eab72c58eec9433513f1219a00a0bfea30fd28@ec2-52-1-92-133.compute-1.amazonaws.com:5432/dds9omudjauuqc'
db = SQLAlchemy(app)

from .EndpointWorker import WeatherEndpointWorker, GeolocatorEndpointWorker

class Gridpoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wfo = db.Column(db.Text)
    grid_x = db.Column(db.Integer)
    grid_y = db.Column(db.Integer)

class Zipcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    gridpoint = db.Column(db.Integer, db.ForeignKey('Gridpoints.id'))

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    forecast = db.Column(db.Text)
    gridpoint = db.Column(db.Integer, db.ForeignKey('Gridpoints.id'))


@app.route("/")
def get_weather():
    weather_worker = WeatherEndpointWorker()
    wfo, grid_x, grid_y = weather_worker.get_gridpoint(41.801990, -70.595630)
    forecast = weather_worker.get_forecast(wfo, grid_x, grid_y)
    return forecast["properties"]["periods"][0]
