from flask import Blueprint, jsonify
from DataGateway import DataGateway
from Publisher import Publisher
import time

data_analyzer_bp = Blueprint("data_analyzer", __name__)

def get_forecast(zip_code: str) -> str:
    gateway = DataGateway()

    zip_code_entry = gateway.find_zipcode(zip_code)
    while zip_code_entry is None:
        pub = Publisher()
        pub.send_zipcode(zip_code)
        time.sleep(3)
        zip_code_entry = gateway.find_zipcode(zip_code)

    full_forecast = gateway.find_simple_forecast(zip_code_entry.zone)
        
    print('get forecast success')
    return [forecast.as_dict() for forecast in full_forecast]

@data_analyzer_bp.route("/forecast/<zip_code>")
def forecast(zip_code):
    return jsonify(get_forecast(zip_code))
