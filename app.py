from flask import Flask, request, make_response
from src.personClass import Person
import os

app = Flask(__name__)


@app.route("/")
def index():
    return "Lab1 persons"

@app.route('/api/v1/persons/<int:person_id>', methods=["GET"])
def get_person(person_id):
    person = Person()
    person_json = person.get_person(person_id)
    if person_json is None:
        return make_response(f"Not found Person for ID {person_id}", 404)
    response = make_response(person_json, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/v1/persons', methods=["GET"])
def get_all_person():
    person = Person()
    persons_json = person.get_all_persons()
    response = make_response(persons_json, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/v1/persons', methods=["POST"])
def post_person():
    new_person = request.json()
    person = Person()
    person_id = person.create_person(new_person)
    if person_id is None:
        return make_response('Invalid data', 400)

    return '', 201, {'location': f'{request.host_url}api/v1/persons/{person_id}'}

@app.route('/api/v1/persons/<int:person_id>', methods=["PATCH"])
def patch_person(person_id):
    new_person = request.get_json()
    person = Person()
    code = person.update_person(new_person, person_id)
    if code:
        return make_response(f'Not found Person for ID {person_id}', 404)
    person_json = person.get_person(person_id)
    response = make_response(person_json, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/api/v1/persons/<int:person_id>', methods=["DELETE"])
def delete_person(person_id):
    person = Person()
    answer = person.delete_person(person_id)
    if answer == 0:
        return make_response(f'Person for ID {person_id} not found', 404)
    return make_response(f'Person for ID {person_id} was removed', 204)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)