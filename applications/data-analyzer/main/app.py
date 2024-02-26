from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/forecast")
def forecast():
    return jsonify(['Sunny', 'Partly Cloudy', 'Rain', 'Snow'])