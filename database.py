import sqlite3
import environment

def connectToDB(file=environment.db_file):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    return connection, cursor

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()

def typeConversionSQL(val):
    if type(val)==int:
        return str(val)
    return chr(39)+val+chr(39)

def listColumns(table):
    connection, cursor = connectToDB()
    cursor.execute(f"PRAGMA table_info({table});")
    columnsInfo = cursor.fetchall()
    closeConnection(connection, cursor)
    return [column[1] for column in columnsInfo]

def selectAllColumn(column, table):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT {column} FROM {table};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return [x for i in results for x in i]

def selectAll(table):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {table};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {result[0]:result[1] for result in results}

def addTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"INSERT INTO {environment.db_table_tasks} (task_id) VALUES ('{task_id}');")
    connection.commit()
    closeConnection(connection, cursor)

def completeTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"UPDATE {environment.db_table_tasks} SET status = 1 WHERE task_id = '{task_id}';")
    connection.commit()
    closeConnection(connection, cursor)

def statusTask(task_id):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {environment.db_table_tasks} WHERE task_id = '{task_id}';")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return {"task_id": results[0][0], "status": results[0][1]}