import sqlite3
from time import time_ns

import environment


def connect_to_db(file = environment.DB_FILE):
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

def update_row(table, column, new_value, s_column, s_value):
    connection, cursor = connect_to_db()
    cursor.execute(f"UPDATE {table} SET {column} = '{new_value}' WHERE {s_column} = '{s_value}';")
    connection.commit()
    close_connection(connection, cursor)

def get_table(table):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {table};")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results

def get_row(table, s_column, s_value):
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {table} WHERE {s_column} = '{s_value}';")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return results[0] if results else []

# UPDATE ROWS
def complete_task(task_id, res):
    update_row(environment.DB_TABLE_TASKS, "status", 1, "task_id", task_id)
    update_row(environment.DB_TABLE_TASKS, "result", res, "task_id", task_id)

def pending_task(task_id, pc):
    update_row(environment.DB_TABLE_TASKS, "status", 2, "task_id", task_id)
    update_row(environment.DB_TABLE_TASKS, "pc", pc, "task_id", task_id)

def free_scheduler(pc):
    update_row(environment.DB_TABLE_SCHEDULER, "status", 0, "pc", pc)

def busy_scheduler(pc):
    update_row(environment.DB_TABLE_SCHEDULER, "status", 1, "pc", pc)

# STATUS/INFO
def list_task(identifier = ''):
    connection, cursor = connect_to_db()
    if identifier == 'all':
        cursor.execute(f"SELECT * FROM {environment.DB_TABLE_TASKS};")
    else:
        cursor.execute(f"SELECT * FROM {environment.DB_TABLE_TASKS} WHERE uuid = '{identifier}';")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return {result[0]:{'status': result[1], 'unix_time': result[2], 'pc': result[3], 'input_values': result[4], 'result': result[5], 'uuid': result[6]} for result in results}

def status_task(task_id):
    result = get_row(environment.DB_TABLE_TASKS, "task_id", task_id)
    return {result[0]:{'status': result[1], 'unix_time': result[2], 'pc': result[3], 'input_values': result[4], 'result': result[5], 'uuid': result[6]}}

def list_scheduler():
    result = get_table(environment.DB_TABLE_SCHEDULER)
    return {r[0]:r[1] for r in result}

def status_scheduler(pc):
    result = get_row(environment.DB_TABLE_SCHEDULER, "pc", pc)
    return {result[0]:result[1]}

def user_info(s_column, s_value):
    result = get_row(environment.DB_TABLE_USERS, s_column, s_value)
    return {'uuid': result[0]}

def user_hash(identifier):
    result = get_row(environment.DB_TABLE_USERS, "uuid", identifier)
    return result[1]

# ADD ROWS
def add_task(task_id, input_values, identifier = ''):
    connection, cursor = connect_to_db()
    cursor.execute(f"INSERT INTO {environment.DB_TABLE_TASKS} (task_id, unix_time, input_values, uuid) VALUES ('{task_id}', {time_ns()}, '{input_values}', '{identifier}');")
    connection.commit()
    close_connection(connection, cursor)
    return status_task(task_id)

def add_user(identifier, hashed_password):
    connection, cursor = connect_to_db()
    cursor.execute(f"INSERT INTO {environment.DB_TABLE_USERS} VALUES ('{identifier}', '{hashed_password}');")
    connection.commit()
    close_connection(connection, cursor)

# RANDOMIZERS
def oldest_pending_task():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.DB_TABLE_TASKS} WHERE status = 0 ORDER BY unix_time ASC LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None

def random_free_scheduler():
    connection, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {environment.DB_TABLE_SCHEDULER} WHERE status = 0 ORDER BY RANDOM() LIMIT 1;")
    results = cursor.fetchall()
    close_connection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None
