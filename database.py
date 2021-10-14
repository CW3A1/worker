import sqlite3
import os

fileName=os.getenv('db_file')
tableName=os.getenv('db_table')

def connectToDB(file=fileName, table=tableName):
    connection = sqlite3.connect(fileName)
    cursor = connection.cursor()
    return connection, cursor

def closeConnection(connection, cursor):
    cursor.close()
    connection.close()

def typeConversionSQL(val):
    if type(val)==int:
        return str(val)
    return chr(39)+val+chr(39)

def listColumns(table=tableName):
    connection, cursor = connectToDB()
    cursor.execute(f"PRAGMA table_info({table});")
    columnsInfo = cursor.fetchall()
    closeConnection(connection, cursor)
    return [column[1] for column in columnsInfo]

def selectAllColumn(column, table=tableName):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT {column} FROM {table};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return [x for i in results for x in i]

def selectAll(table=tableName):
    connection, cursor = connectToDB()
    cursor.execute(f"SELECT * FROM {table};")
    results = cursor.fetchall()
    closeConnection(connection, cursor)
    return results

def insertIntoTable(values, table=tableName):
    connection, cursor = connectToDB()
    cursor.execute(f"INSERT INTO {table} ({', '.join(listColumns(table))}) VALUES ({', '.join([typeConversionSQL(x) for x in values])});")
    connection.commit()
    closeConnection(connection, cursor)

def insertIntoColumns(values, columns, table=tableName):
    connection, cursor = connectToDB()
    cursor.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join([typeConversionSQL(x) for x in values])});")
    connection.commit()
    closeConnection(connection, cursor)