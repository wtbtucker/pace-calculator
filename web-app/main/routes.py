#!/usr/bin/env python3

from flask import request, render_template, Blueprint
import requests

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/forecast", methods=["POST"])
def forecast():
    if request.method == "POST":
        input_text = request.form.get("user_zip_code", "")
        forecast = requests.get(f"http://localhost:5001/forecast/{input_text}")
        print("Get forecast status code: " + str(forecast.status_code))
        # TODO: pass and format template for 7 day forecast instead of just first entry
        return render_template('forecast.html', user_zip_code = input_text, forecast=forecast.text)
    else:
        return "404 not found"

@main.route("/about")
def about():
    return render_template('about.html')

