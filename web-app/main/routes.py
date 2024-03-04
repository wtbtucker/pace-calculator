#!/usr/bin/env python3
from flask import request, render_template, Blueprint
import requests
from backend.Metrics import zipcode_metric
from prometheus_client import generate_latest

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/forecast", methods=["POST"])
def forecast():
    if request.method == "POST":
        input_text = request.form.get("user_zip_code", "")
        zipcode_metric.labels(zipcode=input_text).inc()
        forecast = requests.get(f"https://pace-calculator-analyzer.onrender.com/forecast/{input_text}")
        print("Get forecast status code: " + str(forecast.status_code))
        return render_template('forecast.html', user_zip_code = input_text, forecast=forecast.json())
    else:
        return "404 not found"

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/metrics")
def metrics():
    return generate_latest()

