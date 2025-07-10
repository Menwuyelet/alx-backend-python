import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, param):
        self.db_name = db_name
        self.query = query
        self.param = param
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self
    
    def queryExecution(self):
        cursor = self.conn.cursor()
        cursor.execute(self.query, (self.param,))
        return cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type:
                print(f"An error occurred accessing the the db. Rolling back the db state.")
                self.conn.rollback()
            else:
                print(f"The db has been successfully accessed. Committing changes.")
                self.conn.commit()
        
            self.conn.close()


with ExecuteQuery('users.db', 'SELECT * FROM users WHERE age > ?', '25') as db:
    result = db.queryExecution()
    for row in result:
        print(row)