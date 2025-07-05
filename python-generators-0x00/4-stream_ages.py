import mysql.connector

def stream_user_ages():
    connection = mysql.connector.connect(
        host='localhost',
        user='Nafiad',
        password='Nafiad@mysql12',
        database='ALX_prodev'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        average = 0
    else:
        average = total_age / count

    print(f"Average age of users: {average:.2f}")
