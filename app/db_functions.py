import re
import sqlite3

from app.paths import DB_PATH


def query_db(sql_query, params=(), db_path=DB_PATH):
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        yield from con.execute(sql_query, params)
    con.close()


def get_person_names():
    sql = 'SELECT name FROM Person'
    for row in query_db(sql):
        yield row['name']


def get_meter_data(name):
    sql = '''
        SELECT Meter.date, Meter.height 
        FROM Person 
        INNER JOIN Meter ON Meter.person=Person.id 
        WHERE Person.name=?
    '''
    for row in query_db(sql, (name,)):
        yield dict(row)


def insert_into_meter(data, db_path=DB_PATH):
    name, date, height = data['name'], data['date'], data['height']
    sql = 'SELECT id FROM Person WHERE name=?'
    person_id = next(query_db(sql, (name,), db_path=db_path))['id']

    with sqlite3.connect(db_path) as con:
        sql = 'INSERT INTO Meter (person, date, height) VALUES (?, ?, ?)'
        con.execute(sql, (person_id, date, height))

    con.close()


def entries_exist(table_name, name):
    if not re.match(r'^\w+$', table_name, flags=re.ASCII):
        raise ValueError

    sql = f'''
        SELECT *
        FROM Person
        INNER JOIN {table_name} ON {table_name}.person=Person.id
        WHERE Person.name=?
    '''

    try:
        result = list(query_db(sql, (name,)))
    except sqlite3.OperationalError:
        return False

    return result != []
