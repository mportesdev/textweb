from pathlib import Path

APP_PATH = Path(__file__).resolve().parent.parent

DB_PATH = APP_PATH / 'db' / 'db.sqlite3'
STATIC_PATH = APP_PATH / 'static'
