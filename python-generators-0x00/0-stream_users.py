import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='Nafiad',
        password='Nafiad@mysql12',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)  # Return rows as dicts

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row
    cursor.close()
    connection.close()
