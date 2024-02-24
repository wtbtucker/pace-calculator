from flask import Flask

app = Flask(__name__)

from EndpointWorker import WeatherEndpointWorker, GeolocatorEndpointWorker
from DataGateway import DataGateway

@app.route("/")
def get_weather():
    gateway = DataGateway()
    weather_worker = WeatherEndpointWorker()
    
    zipcode = '02155'
    zipcode_entry = gateway.find_zipcode(zipcode)
    if zipcode_entry is None:
        geo_worker = GeolocatorEndpointWorker()
        lat, long = geo_worker.get_latlng(zipcode)
        wfo, grid_x, grid_y = weather_worker.get_gridpoint(lat, long)
        gateway.insert_gridpoint(wfo, grid_x, grid_y)

        gridpoint = gateway.find_gridpoint(wfo, grid_x, grid_y)
        gateway.insert_zipcode(zipcode, gridpoint)
    else:
        gridpoint_id = zipcode_entry.gridpoint
        gridpoint = gateway.get_gridpoint(gridpoint_id)
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
        start_time = forecast["startTime"]

        gateway.insert_weather(start_time, temperature, dew_point, description, gridpoint.id)

    return full_forecast["properties"]["periods"]
