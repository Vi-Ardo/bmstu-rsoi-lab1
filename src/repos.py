import psycopg2

DB_URL = 'postgresql://vi_ardo:7jJHfq3nzBjQ1PosqgISffUV5sklYBHy@dpg-cukcm1lumphs73bcc7h0-a/db_lab1'

class DatabaseRequests:
    def __init__(self):
        self.DB_URL = DB_URL
        try:
            if not self.check_persons_table():
                self.create_table()
        except Exception as e:
            print(f"Ошибка при инициализации БД: {e}")

    def check_persons_table(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query)
                return any(table[0] == "persons" for table in cursor.fetchall())
        except Exception as e:
            print(f"Ошибка при проверке таблицы: {e}")
            return False

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS persons (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            age INTEGER,
            address VARCHAR(50),
            work VARCHAR(50)
        );
        '''
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

    def get_person(self, person_id):
        query = "SELECT * FROM persons WHERE id = %s;"
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query, (person_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return None

    def get_all_persons(self):
        query = "SELECT * FROM persons;"
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении списка людей: {e}")
            return []

    def add_person(self, new_person):
        query = "INSERT INTO persons (name, address, work, age) VALUES (%s, %s, %s, %s) RETURNING id;"
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query, (new_person['name'], new_person['address'], new_person['work'], new_person['age']))
                conn.commit()
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Ошибка при добавлении человека: {e}")
            return None

    def update_person(self, new_info, person_id):
        query = '''
        UPDATE persons
        SET name = %s, address = %s, work = %s, age = %s
        WHERE id = %s
        RETURNING id, name, age, address, work;
        '''
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query, (new_info['name'], new_info['address'], new_info['work'], new_info['age'], person_id))
                conn.commit()
                return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return None

    def delete_person(self, person_id):
        query = "DELETE FROM persons WHERE id = %s;"
        try:
            with psycopg2.connect(self.DB_URL) as conn, conn.cursor() as cursor:
                cursor.execute(query, (person_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Ошибка при удалении человека: {e}")
            return False