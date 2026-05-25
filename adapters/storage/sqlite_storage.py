from ports.data_repository import GameDataPort

class SQLiteAdapter(GameDataPort):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    