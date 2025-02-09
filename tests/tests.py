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
    "name": "Person2",
    "address": "Hostel",
    "work": "none",
    "age": 15
}

# Данные для обновления
patch_name = {"name": "Anton"}
patch_address = {"address": "Novgorod"}
patch_work = {"work": "Worker"}
patch_age = {"age": 40}

# Некорректные данные (для теста ошибок)
invalid_person = {
    "name": 123,  # Имя должно быть строкой
    "address": None,  # Поле не должно быть пустым
    "work": "",  # Пустая строка может быть запрещена
    "age": "twenty"  # Возраст должен быть числом
}

# Базовый URL
BASE_URL = "https://bmstu-rsoi-lab1-64nw.onrender.com/api/v1/persons"

@pytest.mark.parametrize("persons", [person1, person2])
def test_post_get(persons):
    r = requests.post(url=BASE_URL, json=persons, headers={"Content-Type": "application/json"})
    assert r.status_code == 201

    redirected_url = r.headers['Location']
    person_id = int(redirected_url.split("/")[-1])
    person_id_dict = {"id": person_id}

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
    r = requests.post(url=BASE_URL, json=persons, headers={"Content-Type": "application/json"})
    assert r.status_code == 201

    redirected_url = r.headers['Location']

    r = requests.patch(url=redirected_url, json=patch_var, headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    assert patch_var.items() <= r.json().items()

@pytest.mark.parametrize("persons", [person1, person2])
def test_post_delete(persons):
    r = requests.post(url=BASE_URL, json=persons, headers={"Content-Type": "application/json"})
    assert r.status_code == 201

    redirected_url = r.headers['Location']

    r = requests.delete(redirected_url)
    assert r.status_code == 204

    r = requests.get(redirected_url)
    assert r.status_code == 404

def test_get_nonexistent_person():
    r = requests.get(f"{BASE_URL}/999999")  # ID, который явно не существует
    assert r.status_code == 404

def test_post_invalid_data():
    r = requests.post(url=BASE_URL, json=invalid_person, headers={"Content-Type": "application/json"})
    assert r.status_code == 400