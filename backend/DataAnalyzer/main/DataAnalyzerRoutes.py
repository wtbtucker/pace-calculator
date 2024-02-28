from flask import Blueprint, jsonify
from extensions import db
from backend.DataGateway import DataGateway

data_analyzer_bp = Blueprint("data_analyzer", __name__)

def get_forecast(zip_code: str) -> str:
    gateway = DataGateway()
    zip_code_entry = gateway.find_zipcode(zip_code)
    full_forecast = gateway.find_weather(zip_code_entry.gridpoint)
    return full_forecast.forecast


@data_analyzer_bp.route("/forecast")
def forecast():
    return get_forecast('02155')
