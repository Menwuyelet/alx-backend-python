import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='Nafiad',
        password='Nafiad@mysql12'
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()


def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='Nafiad',
        password='Nafiad@mysql12',
        database='ALX_prodev'
    )

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        PRIMARY KEY (user_id),
        INDEX idx_user_id (user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

def insert_data(connection, filename):
    cursor = connection.cursor()

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row.get('user_id')
            if not user_id:
                user_id = str(uuid.uuid4())
            name = row.get('name')
            email = row.get('email')
            age = row.get('age')

            try:
                age = float(age)
            except Exception:
                age = 0

            cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id = %s", (user_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
                print(f"Inserted user_id {user_id}")
            else:
                print(f"user_id {user_id} already exists, skipping.")
    connection.commit()
    cursor.close()


def main():
    conn = connect_db()
    create_database(conn)
    conn.close()
    conn = connect_to_prodev()
    create_table(conn)
    insert_data(conn, 'user_data.csv')

    conn.close()

if __name__ == "__main__":
    main()