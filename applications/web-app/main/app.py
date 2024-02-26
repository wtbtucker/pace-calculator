#!/usr/bin/env python3

from flask import Flask, request, render_template
from markupsafe import escape
import requests

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/forecast", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_zip_code", "")
    forecast = requests.get('http://localhost:2000/forecast')
    return render_template('forecast.html', user_zip_code = input_text, forecast=forecast)

@app.route("/about")
def about():
    return render_template('about.html')

