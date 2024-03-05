import pytest
from Models import Zipcodes
from backend.components.DataCollectorRoutes import split_zone_url
from backend.components.DataCollectorRoutes import handle_new_zipcode, handle_existing_zipcode, fetch_and_insert_forecast

def test_split_zone_url():
        zone_url = "https://api.weather.gov/zones/forecast/MAZ014"
        id, feature = split_zone_url(zone_url)
        assert id == "MAZ014"
        assert feature == "forecast"

class TestRoutes:
    def setup_method(self):
         self.zipcode_entry = Zipcodes(code='02155', zone='MAZ014')
    

    def test_handle_new_zipcode(self, mock_geo_worker, mock_weather_worker, mock_gateway):
        zipcode = handle_new_zipcode(mock_gateway, mock_weather_worker, mock_geo_worker, '02155')

        # Mock call assertions
        mock_geo_worker.get_latlng.assert_called_once_with('02155')
        mock_weather_worker.get_point.assert_called_once_with(42.4224, -71.1087)
        mock_gateway.insert_zone.assert_called_once_with('MAZ014', 'forecast')

        # return value assertions
        assert zipcode.code == '02155'

    def test_handle_existing_zipcode(self, mock_gateway) -> None:
        zone_id, zone_type = handle_existing_zipcode(self.zipcode_entry, mock_gateway)

        # Mock call assertions
        mock_gateway.get_zone.assert_called_once_with('MAZ014')

        # return value assertions
        assert zone_id == 'MAZ014'
        assert zone_type == 'forecast'

    def test_fetch_and_insert_forecast(self, mock_gateway, mock_weather_worker) -> None:
        simple_forecast = fetch_and_insert_forecast(mock_gateway, mock_weather_worker, 'MAZ014', 'forecast')

        # Mock call assertions
        mock_weather_worker.get_forecast.assert_called_once_with('MAZ014', 'forecast')
        mock_gateway.insert_simple_forecast.assert_called_with({'number': 12, 'name': 'Wednesday Night and Thursday', 'detailedForecast': 'Showers likely. Lows in the mid 40s. Highs in the lower 50s. Chance of rain 60 percent.'}, 'MAZ014')

        # return value assertions
        assert simple_forecast == [{'number': 1, 'name': 'Tonight', 'detailedForecast': 'Mostly clear. Lows in the lower 20s. West winds 15 to 20 mph. Gusts up to 40 mph, decreasing to 25 mph after midnight.'}, {'number': 2, 'name': 'Friday', 'detailedForecast': 'Sunny. Highs in the mid 40s. Southwest winds 5 to 10 mph. Gusts up to 20 mph in the afternoon.'}, {'number': 3, 'name': 'Friday Night', 'detailedForecast': 'Mostly clear in the evening, then becoming partly cloudy. Lows in the lower 30s. Southwest winds 5 to 10 mph with gusts up to 20 mph.'}, {'number': 4, 'name': 'Saturday', 'detailedForecast': 'Rain showers likely. Highs around 50. South winds 5 to 10 mph. Chance of rain 70 percent.'}, {'number': 5, 'name': 'Saturday Night', 'detailedForecast': 'Showers. Not as cool. Near steady temperature in the mid 40s. Southeast winds 5 to 10 mph. Chance of rain 80 percent.'}, {'number': 6, 'name': 'Sunday', 'detailedForecast': 'Cloudy with a 40 percent chance of showers. Near steady temperature in the upper 40s.'}, {'number': 7, 'name': 'Sunday Night', 'detailedForecast': 'Mostly cloudy with a 30 percent chance of showers. Lows in the mid 40s.'}, {'number': 8, 'name': 'Monday and Monday Night', 'detailedForecast': 'Mostly cloudy. Highs in the lower 50s. Lows in the lower 40s.'}, {'number': 9, 'name': 'Tuesday', 'detailedForecast': 'Cloudy with a 30 percent chance of showers. Highs in the mid 50s.'}, {'number': 10, 'name': 'Tuesday Night', 'detailedForecast': 'Mostly cloudy with a 30 percent chance of showers. Lows in the mid 40s.'}, {'number': 11, 'name': 'Wednesday', 'detailedForecast': 'Mostly cloudy with a 50 percent chance of showers. Highs in the upper 50s.'}, {'number': 12, 'name': 'Wednesday Night and Thursday', 'detailedForecast': 'Showers likely. Lows in the mid 40s. Highs in the lower 50s. Chance of rain 60 percent.'}]


if __name__ == "__main__":
    retcode = pytest.main()