import requests

class WeatherEndpointWorker:
    def __init__(self):
        pass

    def get_point(self, lat: float, lng: float) -> str:
        res = requests.get(f"https://api.weather.gov/points/{lat},{lng}")
        print("Point request status code: " + str(res.status_code))
        properties = res.json()["properties"]
        return properties["forecastZone"], properties["gridId"], properties["gridX"], properties["gridY"]
    
    def get_forecast(self, zone_id: str, type: str) -> str:
        res = requests.get(f"https://api.weather.gov/zones/{type}/{zone_id}/forecast")
        print("Forecast status code: " + str(res.status_code))
        return res.json()
    
    def get_weather(self, wfo: str, grid_x: int, grid_y: str) -> str:
        res = requests.get(f"https://api.weather.gov/gridpoints/{wfo}/{grid_x},{grid_y}/forecast/hourly")
        print("Weather status code: " + str(res.status_code))
        return res.json()
    
    def get_zones(self) -> str:
        res = requests.get("https://api.weather.gov/zones")
        print("Zones status code: " + str(res.status_code))
        return res.json()["features"]

class GeolocatorEndpointWorker:
    def __init__(self):
        pass
    
    def get_latlng(self, zip_code: str) -> str:
        api_key = 'd3857ffcbdaafd5ed01c1989e2ee13aa'
        res = requests.get(f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},US&appid={api_key}")
        print("Geolocator status code: " + str(res.status_code))
        message = res.json()
        lat = message['lat']
        long = message['lon']
        return (lat, long)

