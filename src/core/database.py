"""
This module provides functions for interacting with SQLite databases.

It includes operations such as creating and connecting to databases,
executing SQL commands, and performing common database operations.

Constants:
    INT (str): Represents the SQLite INTEGER data type.
    TEXT (str): Represents the SQLite TEXT data type.
"""

from src.core.debug import *

import sqlite3
import sys, os

INT = 'INT'
TEXT = 'TEXT'


def create(file_name: str):
    """
    Create a new SQLite database file.

    Args:
        file_name (str): The name of the database file to create.
    """
    sqlite3.connect(file_name)
    LogDataBaseCreated(file_name)

def connect(file_name: str) -> sqlite3.Connection:
    """
    Connect to an existing SQLite database file.

    Args:
        file_name (str): The name of the database file to connect to.

    Returns:
        sqlite3.Connection: A connection object to the database.

    Raises:
        FileExistsError: If the specified database file does not exist.
    """
    try:
        if not os.path.exists(file_name):
            raise FileExistsError
        conn = sqlite3.connect(file_name)
        LogDataBaseConnect(file_name)
        return conn
    except:
        LogDataBaseNotConnected(file_name)

def close(connection: sqlite3.Connection):
    """
    Close the database connection.

    Args:
        connection (sqlite3.Connection): The connection to close.
    """
    connection.close()

def get_cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    """
    Get a cursor object from a database connection.

    Args:
        connection (sqlite3.Connection): The database connection.

    Returns:
        sqlite3.Cursor: A cursor object for executing SQL commands.
    """
    return connection.cursor()

def execute(cursor: sqlite3.Cursor, connection: sqlite3.Connection, command: str):
    """
    Execute an SQL command and commit the changes.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection to commit changes.
        command (str): The SQL command to execute.
    """
    cursor.execute(command)
    connection.commit()

def execute_table_create(cursor: sqlite3.Cursor, connection: sqlite3.Connection,
                         table_name: str, querys: list[str], types: list[str]):
    """
    Create a new table in the database if it doesn't exist.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection to commit changes.
        table_name (str): The name of the table to create.
        querys (list[str]): A list of column names for the table.
        types (list[str]): A list of data types corresponding to the columns.
    """
    command = f'CREATE TABLE IF NOT EXISTS {table_name}'
    command += '('
    for i in range(len(querys)):
        command += querys[i]
        command += ' '
        command += types[i]
        if i != len(querys) - 1:
            command += ','
    command += ');'
    
    execute(cursor, connection, command)

def execute_get_all_info(cursor: sqlite3.Cursor, connection: sqlite3.Connection, table_name: str):
    """
    Retrieve all information from a specified table.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection.
        table_name (str): The name of the table to retrieve information from.

    Returns:
        list: A list of all rows in the specified table.
    """
    command = f'SELECT * FROM {table_name};'
    execute(cursor, connection, command)
    return cursor.fetchall()

def execute_add_info(cursor: sqlite3.Cursor, connection: sqlite3.Connection, table_name: str, info: list):
    """
    Add a new row of information to a specified table.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection to commit changes.
        table_name (str): The name of the table to add information to.
        info (list): A list of values to insert into the table.
    """
    info_len = len(info)

    wait_string = ''
    for i in range(info_len):
        wait_string += '?'
        if i != info_len - 1:
            wait_string += ','

    cursor.execute(f'INSERT INTO {table_name} VALUES({wait_string})', info)
    connection.commit()

def execute_delete_info(cursor: sqlite3.Cursor, connection: sqlite3.Connection, table_name: str, name: str, date: str):
    """
    Delete a specific row from a table based on user and date.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection to commit changes.
        table_name (str): The name of the table to delete from.
        name (str): The user name to match for deletion.
        date (str): The date to match for deletion.

    Returns:
        list: A list containing a success or error message.
    """
    try:
        command = f'DELETE from {table_name} where user = ? and date = ?'
        cursor.execute(command, (name, date))
        connection.commit()
        LogInformationDeleted(name, date)
        return ['Delete success']
    except:
        return ['Delete error']

def execute_delete_all(cursor: sqlite3.Cursor, connection: sqlite3.Connection, table_name: str):
    """
    Delete all rows from a specified table.

    Args:
        cursor (sqlite3.Cursor): The cursor to execute the command.
        connection (sqlite3.Connection): The database connection to commit changes.
        table_name (str): The name of the table to delete all rows from.

    Returns:
        list: A list containing a success or error message.
    """
    try:
        command = f'DELETE from {table_name}'
        cursor.execute(command)
        connection.commit()
        LogAllInformationDeleted()
        return ['Delete success']
    except:
        return ['Delete error']
