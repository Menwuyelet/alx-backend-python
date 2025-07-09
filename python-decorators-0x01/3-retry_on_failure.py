import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

""" your code goes here"""

def retry_on_failure(retries=3, delay=1):
    def dec(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    result = func(conn, *args, **kwargs)
                    return result
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed with error {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print(f"All attempts failed.")
                        raise 
        return wrapper
    return dec




@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)