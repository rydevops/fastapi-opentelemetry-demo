from fastapi.testclient import TestClient

from poc.application import app

client = TestClient(app)

def test_root_get():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_item():
    item_id = 99
    response  = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id}



