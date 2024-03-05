#!/usr/bin/env python3
from flask import request, render_template, Blueprint
import requests
from Metrics import zipcode_metric
from prometheus_client import generate_latest

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/forecast", methods=["POST"])
def forecast():
    if request.method == "POST":
        zipcode = request.form.get("user_zip_code", "")
        minutes = int(request.form.get("minutes", ""))
        seconds = int(request.form.get("seconds", ""))
        pace_in_seconds = minutes * 60 + seconds
        zipcode_metric.labels(zipcode=zipcode).inc()
        params = {
            'zipcode': zipcode,
            'pace': pace_in_seconds
        }
        print(pace_in_seconds)
        forecast = requests.get(f"https://pace-calculator-analyzer.onrender.com:1000/forecast/", params=params, timeout=3)
        print("Get forecast status code: " + str(forecast.status_code))
        return render_template('forecast.html', user_zip_code = zipcode, forecast=forecast.json())
    else:
        return "404 not found"

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/metrics")
def metrics():
    return generate_latest()

