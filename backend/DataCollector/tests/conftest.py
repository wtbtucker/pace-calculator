import pytest
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

@pytest.fixture()
def client(app):
    return app.test_client()