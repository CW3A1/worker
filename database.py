import sqlite3, environment, time

def connectToDB(file=environment.db_file):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    return connection, cursor

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()

def selectAllColumn(column, table):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT {column} FROM {table};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return [x for i in results for x in i]

def listTask():
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {result[0]:{'status': result[1], 'unix_time': result[2]} for result in results}

def addTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"INSERT INTO {environment.db_table_tasks} (task_id, unix_time) VALUES ('{task_id}', {time.time_ns()});")
    connection.commit()
    closeConnection(connection, cursor)
    return statusTask(task_id)

def completeTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"UPDATE {environment.db_table_tasks} SET status = 1 WHERE task_id = '{task_id}';")
    connection.commit()
    closeConnection(connection, cursor)
    return statusTask(task_id)

def statusTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks} WHERE task_id = '{task_id}';")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {result[0]:{'status': result[1], 'unix_time': result[2]} for result in results}

def listScheduler():
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {result[0]:result[1] for result in results}

def freeScheduler(pc):
    connection, cursor = connectToDB()
    cursor.execute(f"UPDATE {environment.db_table_scheduler} SET status = 0 WHERE pc = '{pc}';")
    connection.commit()
    closeConnection(connection, cursor)
    return statusScheduler(pc)

def busyScheduler(pc):
    connection, cursor = connectToDB()
    cursor.execute(f"UPDATE {environment.db_table_scheduler} SET status = 1 WHERE pc = '{pc}';")
    connection.commit()
    closeConnection(connection, cursor)
    return statusScheduler(pc)

def statusScheduler(pc):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler} WHERE pc = '{pc}';")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {result[0]:result[1] for result in results}

def oldestPendingTask():
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks} WHERE status = 0 ORDER BY unix_time ASC LIMIT 1;")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None

def randomFreeScheduler():
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_scheduler} WHERE status = 0 ORDER BY RANDOM() LIMIT 1;")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return [result[0] for result in results][0] if len(results) else None