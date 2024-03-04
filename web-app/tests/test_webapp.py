def test_index(client):
    response = client.get("/")
    assert b"<title> Home  - Pace Calculator</title>" in response.data

def test_about(client):
    response = client.get("/about")
    assert b"<title> About  - Pace Calculator</title>" in response.data

def test_forecast(client):
    response = client.post("/forecast", data={"user_zip_code": "01867"})

    assert b"<h3>Forecast for 01867</h3>" in response.data