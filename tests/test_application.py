from fastapi.testclient import TestClient

from poc import application

client = TestClient(application.app)

def test_root_get():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_item():
    item_id = 99
    response  = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id}

def test_encode_decode_jwt():
    payload = {"username": "test"}
    encoded_jwt = application.encode_jwt(payload, application.jwt_secret)
    decoded_jwt = application.decode_jwt(encoded_jwt, application.jwt_secret)
    assert payload == decoded_jwt

def test_valid_login():
    auth_payload = {
        "username": "test",
        "password": "test",
    }

    jwt_payload = {
        "username": "test",
    }

    response = client.post("/login", json=auth_payload)
    token = response.json().get('token')

    assert response.status_code == 200
    assert token != None
    assert jwt_payload == application.decode_jwt(token, application.jwt_secret)

def test_invalid_login():
    auth_payload = {
        "username": "test1",
        "password": "test1",
    }

    response = client.post("/login", json=auth_payload)

    assert response.status_code == 403
    assert response.json().get('detail') == 'Invalid username/password'

    auth_payload["username"] = "test"

    response = client.post("/login", json=auth_payload)

    assert response.status_code == 403
    assert response.json().get('detail') == 'Invalid username/password'