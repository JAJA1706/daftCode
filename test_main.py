from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
def test_receive_something():
    response = client.post("/patient", json={'name': 'NAME', 'surename': 'NAZWISKO'})
    assert response.json() == {"received": {'name': 'NAME', 'surename': 'NAZWISKO'}}