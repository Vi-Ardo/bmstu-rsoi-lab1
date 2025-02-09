from src.repos import DatabaseRequests

class Person:
    def __init__(self):
        self.request_db = DatabaseRequests()

    def person_from_tuple(self, tuple_db):
        if not tuple_db or len(tuple_db) != 5:
            raise ValueError("Expected tuple of length 5")
        return {
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
        return self.person_from_tuple(tuple_db)

    def get_all_persons(self):
        tuples_db = self.request_db.get_all_persons()
        persons = []
        if not tuples_db:
            return []
        for i in tuples_db:
            persons.append(self.person_from_tuple(i))
        return persons

    def create_person(self, person):
        person_id = self.request_db.add_person(person)
        return person_id if person_id else None

    def update_person(self, new_person, person_id):
        tuple_db = self.request_db.get_person(person_id)
        if not tuple_db:
            return 1  # Person not found

        updated_person = {**self.person_from_tuple(tuple_db), **new_person}
        self.request_db.update_person(updated_person, person_id)
        return 0  # Success

    def delete_person(self, person_id):
        deleted = self.request_db.delete_person(person_id)
        return 1 if deleted else 0