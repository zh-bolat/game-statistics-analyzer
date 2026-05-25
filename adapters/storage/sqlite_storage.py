import sqlite3

from ports.data_repository import GameDataPort

class SQLiteAdapter(GameDataPort):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
