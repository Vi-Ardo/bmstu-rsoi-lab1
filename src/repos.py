import psycopg2

DB_URL = 'postgresql://vi_ardo:7jJHfq3nzBjQ1PosqgISffUV5sklYBHy@dpg-cukcm1lumphs73bcc7h0-a.frankfurt-postgres.render.com/db_lab1'

class DatabaseRequests:
    def __init__(self):
        self.DB_URL = DB_URL
        if not self.check_persons_table():
            self.create_table()

    def check_persons_table(self):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        for table in cursor.fetchall():
            if table[0] == "persons":
                cursor.close()
                connection.close()
                return True
        cursor.close()
        connection.close()
        return False

    def create_table(self):
        new_table = '''
                    CREATE TABLE persons
                    (
                       id serial primary key,
                       name varchar(50) not null,
                       age integer,
                       address varchar(50),
                       work varchar(50)
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(new_table)
        connection.commit()
        cursor.close()
        connection.close()

    def get_person(self, person_id):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * From persons WHERE id={person_id};")
        person = cursor.fetchone()
        cursor.close()
        connection.close()
        return person

    def get_all_persons(self):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute("SELECT * From persons;")
        persons = cursor.fetchall()
        cursor.close()
        connection.close()
        return persons

    def add_person(self, new_person):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO persons (name, address, work, age) VALUES ('{new_person['name']}', "
                       f"'{new_person['address']}', '{new_person['work']}', '{new_person['age']}') RETURNING id;")
        connection.commit()
        person = cursor.fetchone()
        cursor.close()
        connection.close()
        return person[0]

    def update_person(self, new_info, person_id):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(f"UPDATE persons SET name = '{new_info['name']}', address = '{new_info['address']}', "
                       f"work = '{new_info['work']}', age = '{new_info['age']}' "
                       f"WHERE id={person_id} RETURNING id, name, age, address, work;")
        connection.commit()
        person = cursor.fetchone()
        cursor.close()
        connection.close()
        return person

    def delete_person(self, person_id):
        connection = psycopg2.connect(self.DB_URL)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM persons WHERE id={person_id};")
        rows_deleted = cursor.rowcount
        print(rows_deleted)
        connection.commit()
        cursor.close()
        connection.close()
        return rows_deleted