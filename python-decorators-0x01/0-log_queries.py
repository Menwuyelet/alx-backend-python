import sqlite3
import functools
import logging
from datetime import datetime
#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""

#logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(message)s')

def log_queries(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        #logging.info(f"Execution of query function '{func.__name__}' started.")
        print(f"{datetime.now()} - Execution of query function '{func.__name__}' started.")
        # logging.info(f"args = {args}, kwargs = {kwargs}")
        print(f"{datetime.now()} - args = {args}, kwargs = {kwargs}")
        result = func(*args, **kwargs)  
        end_time = datetime.now()
        # logging.info(f"Execution of query function '{func.__name__}'' ended. execution time: {end_time - start_time}s")  
        print(f"{datetime.now()} - Execution of query function '{func.__name__}'' ended. execution time: {end_time - start_time}s")  
        return result
    return wrapper
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")