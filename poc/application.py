from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from opentelemetry import trace, metrics

import random
import string

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
root_counter = meter.create_counter("root_counter", description="Number of root requests")

app = FastAPI()
jwt_secret = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(32))

class Credentials(BaseModel):
    username: str
    password: str

@app.get("/")
async def read_root():
    # Adding additional attributes to a child span
    with tracer.start_as_current_span("root") as root_span:
        root_span.set_attribute("root.value", "test")
        root_counter.add(1)
        return {"Hello": "World"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/login")
async def login(credentials: Credentials):
    # For testing, using hardcode values
    valid_credentials = {
        "test": "test",
    }

    invalid_auth_exception = HTTPException(403, "Invalid username/password")

    received_username = credentials.username
    received_password = credentials.password

    required_password = valid_credentials.get(received_username)

    if required_password is None:
        raise invalid_auth_exception

    if received_password != required_password:
        raise invalid_auth_exception
        
    jwt_payload = {
        "username": received_username,
    }

    return { "token": encode_jwt(jwt_payload, jwt_secret) }
       

def encode_jwt(payload, secret):
    return jwt.encode(payload, secret, "HS256")

def decode_jwt(payload, secret):
    return jwt.decode(payload, secret, "HS256")