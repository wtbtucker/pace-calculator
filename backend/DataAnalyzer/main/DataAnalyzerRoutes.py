from flask import Blueprint, jsonify, request
from DataGateway import DataGateway
from Publisher import Publisher
import time

data_analyzer_bp = Blueprint("data_analyzer", __name__)

class PaceAdjuster:
    def __init__(self, pace: int):
        self.pace = pace
    
    def adjust_pace(self, temperature: float, dew_point: float) -> int:
        combined_conditions = temperature + self._convert_c_to_f(dew_point)
        if combined_conditions <= 100:
            return self.pace
        elif combined_conditions <= 110:
            return int(self.pace * 0.995)
        elif combined_conditions <= 120:
            return int(self.pace * 0.990)
        elif combined_conditions <= 130:
            return int(self.pace * 0.98)
        elif combined_conditions <= 140:
            return int(self.pace * 0.97)
        elif combined_conditions <= 150:
            return int(self.pace * 0.955)
        elif combined_conditions <= 160:
            return int(self.pace * 0.94)
        elif combined_conditions <= 170:
            return int(self.pace * 0.92)
        elif combined_conditions <= 180:
            return int(self.pace * 0.90)
        # running in combined conditions over 180 is not recommended
        else:
            return -1
        
    def _convert_c_to_f(self, temp):
        return (temp * 1.8) + 32
    
    def format_entry(self, entry):
        entry['pace'] = self.adjust_pace(entry['temperature'], entry['dew_point'])
        return entry

def get_forecast(zip_code: str) -> str:
    gateway = DataGateway()

    zip_code_entry = gateway.find_zipcode(zip_code)
    while zip_code_entry is None:
        pub = Publisher()
        pub.send_zipcode(zip_code)
        time.sleep(3)
        zip_code_entry = gateway.find_zipcode(zip_code)

    full_forecast = gateway.find_weather(zip_code_entry.gridpoint)
        
    print('get forecast success')
    return [forecast.as_dict() for forecast in full_forecast]



@data_analyzer_bp.route("/forecast/")
def forecast():
    print("request received")
    zip_code = request.args.get("zipcode")
    print(zip_code)
    pace = int(request.args.get("pace"))
    print(pace)
    forecast = get_forecast(zip_code)
    adjuster = PaceAdjuster(pace)
    res = [adjuster.format_entry(entry) for entry in forecast]
    print(res)
    return jsonify(res)

