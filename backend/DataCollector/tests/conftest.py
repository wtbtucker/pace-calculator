import pytest
from unittest.mock import Mock
from DataCollector.main import create_app
from DataGateway import DataGateway
from Models import Zones
from extensions import db

@pytest.fixture()
def app():
    app = create_app('postgresql://postgres:postgres@localhost:5432/weather_test')
    with app.app_context():
        db.create_all()
        gateway = DataGateway()
        gateway.insert_zone('MAZ014', 'forecast')

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def mock_geo_worker(mocker):
    mock_instance = Mock()
    mock_instance.get_latlng.return_value = (42.4224, -71.1087)
    mocker.patch('backend.DataCollector.main.EndpointWorker.GeolocatorEndpointWorker', mock_instance)
    return mock_instance

@pytest.fixture
def mock_weather_worker(mocker):
    mock_instance = Mock()
    mock_instance.get_zone.return_value = 'https://api.weather.gov/zones/forecast/MAZ014'
    mock_instance.get_forecast.return_value = {'@context': {'@version': '1.1'}, 'type': 'Feature', 'geometry': {'type': 'MultiPolygon', 'coordinates': []}, 'properties': {'zone': 'https://api.weather.gov/zones/forecast/MAZ015', 'updated': '2024-02-29T16:00:00-05:00', 'periods': [{'number': 1, 'name': 'Tonight', 'detailedForecast': 'Mostly clear. Lows in the lower 20s. West winds 15 to 20 mph. Gusts up to 40 mph, decreasing to 25 mph after midnight.'}, {'number': 2, 'name': 'Friday', 'detailedForecast': 'Sunny. Highs in the mid 40s. Southwest winds 5 to 10 mph. Gusts up to 20 mph in the afternoon.'}, {'number': 3, 'name': 'Friday Night', 'detailedForecast': 'Mostly clear in the evening, then becoming partly cloudy. Lows in the lower 30s. Southwest winds 5 to 10 mph with gusts up to 20 mph.'}, {'number': 4, 'name': 'Saturday', 'detailedForecast': 'Rain showers likely. Highs around 50. South winds 5 to 10 mph. Chance of rain 70 percent.'}, {'number': 5, 'name': 'Saturday Night', 'detailedForecast': 'Showers. Not as cool. Near steady temperature in the mid 40s. Southeast winds 5 to 10 mph. Chance of rain 80 percent.'}, {'number': 6, 'name': 'Sunday', 'detailedForecast': 'Cloudy with a 40 percent chance of showers. Near steady temperature in the upper 40s.'}, {'number': 7, 'name': 'Sunday Night', 'detailedForecast': 'Mostly cloudy with a 30 percent chance of showers. Lows in the mid 40s.'}, {'number': 8, 'name': 'Monday and Monday Night', 'detailedForecast': 'Mostly cloudy. Highs in the lower 50s. Lows in the lower 40s.'}, {'number': 9, 'name': 'Tuesday', 'detailedForecast': 'Cloudy with a 30 percent chance of showers. Highs in the mid 50s.'}, {'number': 10, 'name': 'Tuesday Night', 'detailedForecast': 'Mostly cloudy with a 30 percent chance of showers. Lows in the mid 40s.'}, {'number': 11, 'name': 'Wednesday', 'detailedForecast': 'Mostly cloudy with a 50 percent chance of showers. Highs in the upper 50s.'}, {'number': 12, 'name': 'Wednesday Night and Thursday', 'detailedForecast': 'Showers likely. Lows in the mid 40s. Highs in the lower 50s. Chance of rain 60 percent.'}]}}
    mock_instance.get_zones.return_value = [{'id': 'https://api.weather.gov/zones/county/AKC013'}]
    mocker.patch('backend.DataCollector.main.EndpointWorker.WeatherEndpointWorker', mock_instance)
    return mock_instance

@pytest.fixture
def mock_gateway(mocker):
    mock_instance = Mock()
    mock_instance.get_zone.return_value = Zones(id='MAZ014', type='forecast')
    mocker.patch('DataGateway.DataGateway', mock_instance)
    return mock_instance