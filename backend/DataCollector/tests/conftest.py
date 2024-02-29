import pytest
from unittest.mock import Mock
from DataCollector.main import create_app
from DataGateway import DataGateway
from extensions import db

@pytest.fixture()
def app():
    app = create_app('postgresql://postgres:postgres@localhost/weather_test')
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
    return mocker.patch('backend.DataCollector.main.EndpointWorker.GeolocatorEndpointWorker', mock_instance)

@pytest.fixture
def mock_weather_worker(mocker):
    mock_instance = Mock()
    mock_instance.get_zone.return_value = 'https://api.weather.gov/zones/forecast/MAZ014'
    return mocker.patch('backend.DataCollector.main.EndpointWorker.WeatherEndpointWorker', mock_instance)

@pytest.fixture
def mock_gateway(mocker):
    mock_instance = Mock()
    return mocker.patch('backend.DataGateway', mock_instance)