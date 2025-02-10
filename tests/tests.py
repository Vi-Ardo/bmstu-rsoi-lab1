import requests
import pytest

# Тестовые данные
person1 = {
    "name": "Ivanov Mikhail Olegovich",
    "address": "Moscow",
    "work": "IU7",
    "age": 25
}
person2 = {
    "name": "Petrov",
    "address": "Hostel",
    "work": "Owner",
    "age": 55
}

# Данные для обновления
patch_name = {"name": "Anton"}
patch_address = {"address": "Novgorod"}
patch_work = {"work": "Worker"}
patch_age = {"age": 40}



@pytest.mark.parametrize("persons", [person1, person2])
def test_post_get(persons):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    assert r.status_code == 201
    redirected_url = r.headers['Location']
    person_id_dict = {"id": int(redirected_url.split("/")[-1])}
    r = requests.get(redirected_url)
    assert r.status_code == 200
    assert r.json() == persons | person_id_dict

@pytest.mark.parametrize("persons, patch_var", [
    (person1, patch_name), 
    (person1, patch_address),
    (person2, patch_work), 
    (person2, patch_age)
])
def test_post_patch(persons, patch_var):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    redirected_url = r.headers['Location']
    r = requests.patch(url=redirected_url, json=patch_var)
    print(r.content)
    print(r.json())
    assert r.status_code == 200
    assert patch_var.items() <= r.json().items()

@pytest.mark.parametrize("persons", [person1, person2])
def test_post_delete(persons):
    r = requests.post(url="http://127.0.0.1:8080/api/v1/persons", json=persons)
    redirected_url = r.headers['Location']
    r = requests.delete(redirected_url)
    assert r.status_code == 204
    r = requests.get(redirected_url)
    assert r.status_code == 404
