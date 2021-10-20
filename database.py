import sqlite3
import time

import environment


def connect_to_db(file = environment.db_file):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

def select_all_column(column, table):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT {column} FROM {table};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [x for i in results for x in i]

# TASK FUNCTIONS
def list_task():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return {result[0]:{'status': result[1], 'unix_time': result[2]} for result in results}

def add_task(task_id):
    connection, cursor = connect_to_db()
    cursor.execute(f"INSERT INTO {environment.db_table_tasks} (task_id, unix_time) VALUES ('{task_id}', {time.time_ns()});")
    connection.commit()
    close_connection(connection, cursor)
    return status_task(task_id)

def complete_task(task_id):
    connection, cursor = connect_to_db()
    cursor.execute(f"UPDATE {environment.db_table_tasks} SET status = 1 WHERE task_id = '{task_id}';")
    connection.commit()
    close_connection(connection, cursor)
    return status_task(task_id)

def status_task(task_id):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks} WHERE task_id = '{task_id}';")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return {result[0]:{'status': result[1], 'unix_time': result[2]} for result in results}

def random_free_scheduler():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler} WHERE status = 0 ORDER BY RANDOM() LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None

# SCHEDULER FUNCTIONS
def list_scheduler():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return {result[0]:result[1] for result in results}

def free_scheduler(pc):
    connection, cursor = connect_to_db()
    cursor.execute(f"UPDATE {environment.db_table_scheduler} SET status = 0 WHERE pc = '{pc}';")
    connection.commit()
    close_connection(connection, cursor)
    return status_scheduler(pc)

def busy_scheduler(pc):
    connection, cursor = connect_to_db()
    cursor.execute(f"UPDATE {environment.db_table_scheduler} SET status = 1 WHERE pc = '{pc}';")
    connection.commit()
    close_connection(connection, cursor)
    return status_scheduler(pc)

def status_scheduler(pc):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler} WHERE pc = '{pc}';")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return {result[0]:result[1] for result in results}

def oldest_pending_task():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks} WHERE status = 0 ORDER BY unix_time ASC LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None
