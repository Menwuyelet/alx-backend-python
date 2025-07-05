import mysql.connector

def paginate_users(page_size, offset):
    connection = mysql.connector.connect(
        host='localhost',
        user='Nafiad',
        password='Nafiad@mysql12'
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def lazy_paginate(page_size):
    offset = 0

    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size