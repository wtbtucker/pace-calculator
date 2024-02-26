#!/usr/bin/env python3

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/forecast", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_zip_code", "")
    return "Your zip code: " + input_text