from flask import Blueprint
from EndpointWorker import WeatherEndpointWorker, GeolocatorEndpointWorker
from backend.DataGateway import DataGateway

data_collector_bp = Blueprint("data_collector", __name__)

def split_zone_url(zone_url: str) -> tuple[str, str]:
    "https://api.weather.gov/zones/forecast/MAZ014"
    split_url = zone_url.split('/')
    return (split_url[5], split_url[4])

@data_collector_bp.route("/")
def get_weather():
    gateway = DataGateway()
    weather_worker = WeatherEndpointWorker()
    
    zipcode = '02155'
    zipcode_entry = gateway.find_zipcode(zipcode)
    if zipcode_entry is None:
        geo_worker = GeolocatorEndpointWorker()
        lat, long = geo_worker.get_latlng(zipcode)
        zone_url = weather_worker.get_zone(lat, long)
        zone_id, zone_type = split_zone_url(zone_url)
        gateway.insert_zone(zone_id, zone_type)
        gateway.insert_zipcode(zipcode, zone_id)
    else:
        zone_id = zipcode_entry.zone
        zone = gateway.get_zone(zone_id)
        zone_type = zone.type

    simple_forecast = weather_worker.get_forecast(zone_id, zone_type)
    for period in simple_forecast["properties"]["periods"]:
        gateway.insert_simple_forecast(period, zone_id)

    return simple_forecast["properties"]["periods"]

@data_collector_bp.route("/zones")
def zones():
    worker = WeatherEndpointWorker()
    zone_list = worker.get_zones()
    return [f"{zone['id']}" for zone in zone_list]