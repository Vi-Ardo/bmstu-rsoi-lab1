from src.repos import DatabaseRequests

class Person:
    def __init__(self):
        self.request_db = DatabaseRequests()
        self.person = {
            "id": None,
            "name": None,
            "age": None,
            "address": None,
            "work": None
        }

    def person_from_tuple(self, tuple_db):
        if not tuple_db or len(tuple_db) != 5:
            raise ValueError("Expected tuple of length 5")
        self.person = {
            "id": int(tuple_db[0]),
            "name": str(tuple_db[1]),
            "age": int(tuple_db[2]),
            "address": str(tuple_db[3]),
            "work": str(tuple_db[4])
        }

    def get_person(self, person_id):
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return None
        self.person_from_tuple(tuple_db)
        return self.person

    def get_all_persons(self):
        tuples_db = self.request_db.get_all_persons()
        persons = []
        if not tuples_db:
            return None
        for i in tuples_db:
            self.person_from_tuple(i)
            persons.append(self.person)
        return persons

    def create_person(self, person):
        person_id = self.request_db.add_person(person)
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return None
        return person_id

    def update_person(self, new_person, person_id):
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return 1

        self.person_from_tuple(tuple_db)
        self.person.update(new_person)
        person = self.request_db.update_person(self.person, person_id)
        self.person_from_tuple(person)
        return 0

    def delete_person(self, person_id):
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return 0
        self.request_db.delete_person(person_id)
        return person_id