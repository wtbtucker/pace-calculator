from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/weather'
db = SQLAlchemy(app)

from EndpointWorker import WeatherEndpointWorker, GeolocatorEndpointWorker

class Gridpoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wfo = db.Column(db.Text)
    grid_x = db.Column(db.Integer)
    grid_y = db.Column(db.Integer)

class Zipcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    gridpoint = db.Column(db.Integer, db.ForeignKey(Gridpoints.id))

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    forecast = db.Column(db.Text)
    gridpoint = db.Column(db.Integer, db.ForeignKey(Gridpoints.id))


@app.route("/")
def get_weather():
    with app.app_context():
        db.create_all()

    weather_worker = WeatherEndpointWorker()
    
    zipcode = '02155'
    zipcode_entry = Zipcodes.query.filter_by(code=zipcode).first()
    if zipcode_entry is None:
        geo_worker = GeolocatorEndpointWorker()
        lat, long = geo_worker.get_latlng(zipcode)
        wfo, grid_x, grid_y = weather_worker.get_gridpoint(lat, long)
        new_gridpoint = Gridpoints(wfo=wfo, grid_x=grid_x, grid_y=grid_y)
        db.session.add(new_gridpoint)
        db.session.commit()

        gridpoint = Gridpoints.query.filter_by(wfo=wfo, grid_x=grid_x, grid_y=grid_y).first()
        new_zipcode = Zipcodes(code=zipcode, gridpoint=gridpoint.id)
        db.session.add(new_zipcode)
        db.session.commit()
    else:
        gridpoint_id = zipcode_entry.gridpoint
        gridpoint = Gridpoints.query.get_or_404(gridpoint_id)
        wfo = gridpoint.wfo
        grid_x = gridpoint.grid_x
        grid_y = gridpoint.grid_y

    full_forecast = weather_worker.get_forecast(wfo, grid_x, grid_y)
    for forecast in full_forecast["properties"]["periods"]:
        # dew point in Celsius
        dew_point = forecast["dewpoint"]["value"]
        # temperature in Farenheit
        temperature = forecast["temperature"]
        description = forecast["shortForecast"]

        start_time = datetime.strptime(forecast["startTime"][:19], "%Y-%m-%dT%H:%M:%S")
        print(start_time)

        new_forecast = Weather(start_time=start_time, temperature=temperature, dew_point=dew_point, forecast=description, gridpoint=gridpoint.id)
        db.session.add(new_forecast)
        db.session.commit()

    return full_forecast["properties"]["periods"]
