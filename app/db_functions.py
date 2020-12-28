import sqlite3

from app_paths import DB_PATH


def get_meter_data(name):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    yield from cur.execute('SELECT * FROM meter WHERE name=?', (name,))

    con.close()


def entries_exist(table, name):
    if table != 'meter':
        return False

    data_for_name = list(get_meter_data(name))
    return len(data_for_name) > 0
