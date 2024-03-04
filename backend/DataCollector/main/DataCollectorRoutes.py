from flask import Blueprint, jsonify
from EndpointWorker import WeatherEndpointWorker, GeolocatorEndpointWorker
from DataGateway import DataGateway
from Subscriber import Subscriber
data_collector_bp = Blueprint("data_collector", __name__)
def split_zone_url(zone_url: str) -> tuple[str, str]:
    split_url = zone_url.split('/')
    return split_url[5], split_url[4]


def handle_new_zipcode(gateway: DataGateway, weather_worker: WeatherEndpointWorker,
                       geo_worker: GeolocatorEndpointWorker, zipcode: str) -> tuple[str, str]:
    lat, long = geo_worker.get_latlng(zipcode)
    zone_url = weather_worker.get_zone(lat, long)
    zone_id, zone_type = split_zone_url(zone_url)
    gateway.insert_zone(zone_id, zone_type)
    gateway.insert_zipcode(zipcode, zone_id)
    return zone_id, zone_type


def handle_existing_zipcode(zipcode_entry, gateway: DataGateway) -> tuple[str, str]:
    zone_id = zipcode_entry.zone
    zone = gateway.get_zone(zone_id)
    zone_type = zone.type
    return zone_id, zone_type


def fetch_and_insert_forecast(gateway: DataGateway, weather_worker: WeatherEndpointWorker, zone_id: str,
                              zone_type: str) -> str:
    simple_forecast = weather_worker.get_forecast(zone_id, zone_type)
    for period in simple_forecast["properties"]["periods"]:
        gateway.insert_simple_forecast(period, zone_id)
    return simple_forecast["properties"]["periods"]


@data_collector_bp.route("/")
def get_weather():
    gateway = DataGateway()
    weather_worker = WeatherEndpointWorker()
    geo_worker = GeolocatorEndpointWorker()
    zipcode = '02108'
    zipcode_entry = gateway.find_zipcode(zipcode)
    if zipcode_entry is None:
        zone_id, zone_type = handle_new_zipcode(gateway, weather_worker, geo_worker, zipcode)
    else:
        zone_id, zone_type = handle_existing_zipcode(zipcode_entry, gateway)
    return fetch_and_insert_forecast(gateway, weather_worker, zone_id, zone_type)


@data_collector_bp.route("/zones")
def zones():
    worker = WeatherEndpointWorker()
    zone_list = worker.get_zones()
    return jsonify({'zones': [zone['id'] for zone in zone_list]})

@data_collector_bp.route("/listen")
def listen():
    receiver = Subscriber()
    receiver.listen_for_zipcode()
