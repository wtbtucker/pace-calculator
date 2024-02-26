def test_index(client):
    response = client.get("/")
    assert b"<title> Home  - Pace Calculator</title>" in response.data