from extensions import db
from datetime import datetime

from Models import Zipcodes, Zones, Weather, SimpleForecasts

class DataGateway:
    def __init__(self):
        pass
        
    def insert_zipcode(self, zipcode, zone):
        new_zipcode = Zipcodes(code=zipcode, zone=zone)
        db.session.merge(new_zipcode)
        db.session.commit()

    def insert_zone(self, id, type):
        new_zone = Zones(id=id, type=type)
        db.session.merge(new_zone)
        db.session.commit()

    def insert_weather(self, start_time, temperature, dew_point, description, id):
        formatted_time = self._convert_time(start_time)
        new_forecast = Weather(start_time=formatted_time, temperature=temperature, dew_point=dew_point, forecast=description, zone=id)
        db.session.add(new_forecast)
        db.session.commit()
    
    def insert_simple_forecast(self, period: str, id: str):
        start_time = period["name"]
        weather = period["detailedForecast"]
        new_simple_forecast = SimpleForecasts(start_time=start_time, weather=weather, zone=id)
        db.session.merge(new_simple_forecast)
        db.session.commit()
    
    def find_weather(self, id):
        return Weather.query.filter_by(zone=id).first()

    def find_simple_forecast(self, id):
        return SimpleForecasts.query.filter_by(zone=id).all()
    
    def find_zipcode(self, zipcode):
        return Zipcodes.query.filter_by(code=zipcode).first()
    
    def get_zone(self, id):
        return Zones.query.get_or_404(id)
    
    def _convert_time(self, start_time: str):
        return datetime.strptime(start_time[:19], "%Y-%m-%dT%H:%M:%S")