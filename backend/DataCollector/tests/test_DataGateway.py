from DataGateway import DataGateway
import pytest
from datetime import datetime

from Models import Gridpoints

class TestDataGateway:
    def setup_method(self):
        self.zone = 'MAZ014'
        self.gateway = DataGateway()
        self.gridpoint = Gridpoints(wfo='BOX', grid_x=88, grid_y=98)

    def test_insert_zipcode(self, app):
        valid_zipcode = '01867'
        with app.app_context():
            self.gateway.insert_zipcode(valid_zipcode, self.zone, self.gridpoint)
            zipcode_entry = self.gateway.find_zipcode('01867')
            assert zipcode_entry.code == '01867'

    def test_convert_time(self):
        converted_time = self.gateway._convert_time("2024-02-29T08:00:00-05:00")
        assert converted_time == datetime(2024,2,29,hour=8)


    def test_insert_weather(self, app):
        with app.app_context():
            self.gateway.insert_weather("2024-02-24T10:00:00-05:00",30,-8.33,"Cloudy",self.gridpoint.id)
            weather_entry = self.gateway.find_weather(self.zone)
            assert weather_entry.temperature == 30
            assert weather_entry.dew_point == -8.33

if __name__ == "__main__":
    retcode = pytest.main()