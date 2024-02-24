import pytest
from ..main.DataGateway import DataGateway


class DataGatewayTest:
    def setup_class(self):
        self.gateway = DataGateway()
        self.gateway.insert_gridpoint('BOX', 68, 98)
        self.gridpoint = self.gateway.find_gridpoint('BOX', 68, 98)

    def test_insert_gridpoint(self):
        pass

    def test_insert_zipcode(self):
        valid_zipcode = '01867'
        self.gateway.insert_zipcode(valid_zipcode, self.gridpoint.id)
        zipcode_entry = self.gateway.find_zipcode('01867')
        assert zipcode_entry.code == '01867'

    def test_insert_weather(self):
        self.gateway.insert_weather("2024-02-24T10:00:00-05:00",30,-8.33,"Cloudy",self.gridpoint.id)
        weather_entry = self.gateway.find_weather(self.gridpoint.id)
        assert weather_entry.temperature == 30
        assert weather_entry.dew_point == -8.33

if __name__ == "__main__":
    retcode = pytest.main()