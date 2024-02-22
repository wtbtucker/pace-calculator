import requests

class WeatherEndpointWorker:
    def __init__(self):
        pass

    def get_gridpoint(self, lat: float, lng: float) -> str:
        res = requests.get(f"https://api.weather.gov/points/{lat},{lng}")
        print("Point request status code: " + str(res.status_code))
        properties = res.json()["properties"]
        wfo = properties["gridId"]
        grid_x = properties["gridX"]
        grid_y = properties["gridY"]
        return (wfo, grid_x, grid_y)
    
    
    def get_forecast(self, grid_id: str, grid_x: str, grid_y: str) -> str:
        res = requests.get(f"https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast/hourly")
        print("Forecast status code: " + str(res.status_code))
        return res.json()

class GeolocatorEndpointWorker:
    def __init__(self):
        pass
    
    def get_latlng(zip_code: str) -> str:
        api_key = 'd3857ffcbdaafd5ed01c1989e2ee13aa'
        res = requests.get(f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},US&appid={api_key}")
        print(res.status_code)
        return res.text

