import sqlite3
import json
from datetime import datetime

from core import GameRecord
from ports.data_repository import GameDataPort

class SQLiteAdapter(GameDataPort):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS game_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL,]
            date TEXT NOT NULL,
            import_at TEXT NOT NULL)""")

    def import_from_json(self, json_path: str) -> int:
        with open(json_path,"r",encoding="utf-8") as f:
            raw_data = json.load(f)
        imported_count = 0

        now = datetime.now().strftime("%Y-%m-%d")
        with self._connect() as conn:
            for entry in raw_data:
                try:
                    record = GameRecord(entry["player"],
                                        entry["score"],
                                        entry["date"])
                    conn.execute("""INSERT INTO game_records 
                                 (player, score, date, imported_at)
                                 VALUES (?,?,?,?)""",
                                 (record.player,
                                  record.score,
                                  record.date,
                                  now))
                    imported_count += 1
                except (KeyError,ValueError, TypeError) as e:
                    print(f"[Предупреждение] "
                          f"Запись пропущена {entry} "
                          f"Причина: {e}" )

        print(f"[SQLite] Импортировано {imported_count} записей")

        return imported_count