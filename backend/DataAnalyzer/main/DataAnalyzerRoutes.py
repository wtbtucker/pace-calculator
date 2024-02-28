from flask import Blueprint, jsonify

data_analyzer_bp = Blueprint("data_analyzer", __name__)

@data_analyzer_bp.route("/forecast")
def forecast():
    return jsonify(['Sunny', 'Partly Cloudy', 'Rain', 'Snow'])