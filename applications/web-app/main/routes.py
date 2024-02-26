#!/usr/bin/env python3

from flask import request, render_template, Blueprint
import requests

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/forecast", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_zip_code", "")
    forecast = requests.get('http://localhost:2000/forecast').json()
    return render_template('forecast.html', user_zip_code = input_text, forecast=forecast)

@main.route("/about")
def about():
    return render_template('about.html')

