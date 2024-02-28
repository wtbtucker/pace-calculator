from extensions import db
from datetime import datetime

from Models import Zipcodes, Gridpoints, Weather

class DataGateway:
    def __init__(self):
        pass
        
    def insert_zipcode(self, zipcode, gridpoint):
        new_zipcode = Zipcodes(code=zipcode, gridpoint=gridpoint.id)
        db.session.add(new_zipcode)
        db.session.commit()

    def insert_gridpoint(self, wfo, grid_x, grid_y):
        new_gridpoint = Gridpoints(wfo=wfo, grid_x=grid_x, grid_y=grid_y)
        db.session.add(new_gridpoint)
        db.session.commit()

    def insert_weather(self, start_time, temperature, dew_point, description, id):
        formatted_time = self._convert_time(start_time)
        new_forecast = Weather(start_time=formatted_time, temperature=temperature, dew_point=dew_point, forecast=description, gridpoint=id)
        db.session.add(new_forecast)
        db.session.commit()
    
    def find_weather(self, id):
        return Weather.query.filter_by(gridpoint=id).first()
    
    def find_gridpoint(self, wfo, grid_x, grid_y):
        return Gridpoints.query.filter_by(wfo=wfo, grid_x=grid_x, grid_y=grid_y).first()
    
    def find_zipcode(self, zipcode):
        return Zipcodes.query.filter_by(code=zipcode).first()
    
    def get_gridpoint(self, id):
        return Gridpoints.query.get_or_404(id)
    
    def _convert_time(self, start_time: str):
        return datetime.strptime(start_time[:19], "%Y-%m-%dT%H:%M:%S")
