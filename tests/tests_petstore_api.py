import json
import requests
from jsonschema import validate

base_url = "https://petstore.swagger.io/v2"

def tests_add_pet_to_store():
    payload = {
      "name": "Kitty",
      "status": "available"
    }

    response = requests.post(base_url + "/pet", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Kitty"