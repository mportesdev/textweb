import sqlite3

from app_paths import DB_PATH


def get_person_names():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    for row in cur.execute('SELECT name FROM Person'):
        yield row['name']

    con.close()


def get_meter_data(name):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    yield from cur.execute('SELECT Meter.date, Meter.height '
                           'FROM Person '
                           'INNER JOIN Meter ON Meter.person=Person.id '
                           'WHERE Person.name=?',
                           (name,))

    con.close()


def entries_exist(table_name, name):
    if table_name.casefold() == 'meter':
        return list(get_meter_data(name)) != []

    return False
