from flask import Flask

app = Flask(__name__)

@app.route("/forecast")
def forecast():
    return ['Sunny', 'Partly Cloudy', 'Rain', 'Snow']