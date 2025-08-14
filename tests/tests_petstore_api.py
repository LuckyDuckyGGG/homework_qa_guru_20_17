import pytest
import requests
from jsonschema import validate
from schemas import create_pet, edit_pet, get_pet_by_status, get_store_pet_inventory

base_url = "https://petstore.swagger.io/v2"

@pytest.fixture()
def add_pet_to_store():
    payload = {
        "name": "Kitty",
        "status": "sold"
    }

    response = requests.post(base_url + "/pet", json=payload)
    pet_id = response.json()["id"]

    yield pet_id



def test_add_pet_to_store_post():
    payload = {
      "name": "Kitty",
      "status": "sold"
    }

    response = requests.post(base_url + "/pet", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Kitty"


def test_edit_pet_name_put(add_pet_to_store):
    pet_id = add_pet_to_store
    payload = {
        "id": pet_id,
        "name": "Mouse"
    }

    response = requests.put(base_url + "/pet", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Mouse"

def test_pet_store_inventory_get():
    response = requests.get(base_url + "/store/inventory")

    assert response.status_code == 200

def test_delete_pet(add_pet_to_store):
    pet_id = add_pet_to_store

    response = requests.delete(base_url + f"/pet/{pet_id}")

    assert response.status_code == 200

def test_negative_404_delete_pet():
    pet_id = 2716

    response = requests.delete(base_url + f"/pet/{pet_id}")

    assert response.status_code == 404
    assert response.reason == "Not Found"

def test_method_not_allowed_415():
    response = requests.delete(base_url + f"/pet/")

    assert response.status_code == 405
    assert response.reason == "Method Not Allowed"

def test_unsupported_media_type_415(add_pet_to_store):
    pet_id = add_pet_to_store
    payload = {
        "id": pet_id,
        "name": "Mouse"
    }

    response = requests.put(base_url + "/pet", data=payload)

    assert response.status_code == 415
    assert response.reason == "Unsupported Media Type"

def test_schema_create_pet():
    payload = {
        "name": "Kitty",
        "status": "sold"
    }

    response = requests.post(base_url + "/pet", json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, create_pet)

def test_schema_edit_pet(add_pet_to_store):
    pet_id = add_pet_to_store
    payload = {
        "id": pet_id,
        "name": "Mouse"
    }

    response = requests.put(base_url + "/pet", json=payload)
    body = response.json()

    assert response.status_code == 200
    validate(body, edit_pet)

def test_schema_get_pet_store_inventory(add_pet_to_store):
    pet_id = add_pet_to_store

    response = requests.get(base_url + "/store/inventory")
    body = response.json()

    assert response.status_code == 200
    validate(body, get_store_pet_inventory)

def test_schema_get_pet_by_status():
    response = requests.get(base_url + "/pet/findByStatus", params="sold")
    body = response.json()

    assert response.status_code == 200
    validate(body, get_pet_by_status)





