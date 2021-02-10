import sqlite3

from app_paths import DB_PATH


def query_db(sql_query, params=()):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    yield from cur.execute(sql_query, params)
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


def entries_exist(table_name, name):
    if table_name.casefold() == 'meter':
        return list(get_meter_data(name)) != []

    return False
