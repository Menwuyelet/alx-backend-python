import sqlite3 

class FileOpener:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        return self.conn
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                print("An error occurred. Rolling back the db.")
                self.conn.rollback()
            else:
                print("Committing transaction")
                self.conn.commit()

            self.conn.close()

with FileOpener("users") as db:
    cursor = db.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS users (" \
    # "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    # "name TEXT NOT NULL," \
    # "email TEXT UNIQUE NOT NULL," \
    # "password TEXT NOT NULL)" )
    # cursor.execute("INSERT INTO users (id, name, email, password)" \
    # "VALUES (1, 'nafiad', 'ex@mail.com', '123we;')")
    cursor.execute("SELECT * FROM users")
        