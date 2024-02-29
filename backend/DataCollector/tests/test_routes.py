from backend.DataCollector.main.DataCollectorRoutes import split_zone_url
from backend.DataCollector.main.DataCollectorRoutes import handle_new_zipcode, handle_existing_zipcode, fetch_and_insert_forecast

def test_split_zone_url():
    zone_url = "https://api.weather.gov/zones/forecast/MAZ014"
    id, feature = split_zone_url(zone_url)
    assert id == "MAZ014"
    assert feature == "forecast"

def test_handle_new_zipcode(mock_geo_worker, mock_weather_worker, mock_gateway):
    zone_id, zone_type = handle_new_zipcode(mock_gateway, mock_weather_worker, '02155')

    mock_geo_worker.assert_called_once()
    mock_geo_worker.return_value.get_latlng.assert_called_once_with('02155')
    mock_weather_worker.assert_called_once()
    mock_weather_worker.return_value.get_zone.assert_called_once_with(42.4224, -71.1087)
    mock_gateway.assert_called_once()
    mock_gateway.return_value.insert_zone.assert_called_once_with('MAZ014', 'forecast')
    mock_gateway.return_value.insert_zipcode.assert_called_once_with('02155', 'MAZ014')

    assert zone_id == 'MAZ014'
    assert zone_type == 'forecast'

def test_get_weather(client):
    pass