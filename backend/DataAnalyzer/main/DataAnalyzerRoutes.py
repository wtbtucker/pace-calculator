from flask import Blueprint, jsonify
from DataGateway import DataGateway
from Publisher import Publisher

data_analyzer_bp = Blueprint("data_analyzer", __name__)

def get_forecast(zip_code: str) -> str:
    gateway = DataGateway()
    zip_code_entry = gateway.find_zipcode(zip_code)
    full_forecast = gateway.find_simple_forecast(zip_code_entry.zone)
    print('get forecast success')
    return [forecast.as_dict() for forecast in full_forecast]

@data_analyzer_bp.route("/forecast/<zip_code>")
def forecast(zip_code):
    return jsonify(get_forecast(zip_code))

@data_analyzer_bp.route("/send_message")
def send_message():
    zip_code = '02155'
    pub = Publisher()
    pub.send_zipcode(zip_code)
    return 'success?'
