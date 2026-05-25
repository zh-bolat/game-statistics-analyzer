import os

from adapters.storage.json_storage import JSONFileAdapter
from adapters.ui.cli_app import CLIAdapter
from core.services import StatsAnalyzer
from adapters.storage.sqlite_storage import SQLiteAdapter


def run_cli():
    file_path = os.getenv("DATA_FILE", "data/stats.json")

    storage_type = os.getenv("STORAGE_TYPE", "json").lower()

    print(f"[Загрузка] Читаем данные из: {file_path}")

    if storage_type == "json":
        adapter = JSONFileAdapter(file_path)

    elif storage_type == "sqlite":
        db_path = os.getenv("DB_FILE", "data/stats.db")
        print(f"[SQLite] База данных: {db_path}")
        adapter = SQLiteAdapter(db_path)
        adapter.import_from_json(file_path)
    else:
        print(f"[Ошибка] Неизвестный storage: {storage_type}")
        return

    records = adapter.load_records()
    analyzer = StatsAnalyzer(records)

    cli = CLIAdapter(analyzer)
    cli.run()


def run_web():
    print("Веб-режим: запустите командой ->  streamlit run adapters/ui/streamlit_app.py")

def run_api():
    print("API-режим: запустите командой -> uvicorn adapters.ui.fastapi_app:app --reload")

if __name__ == "__main__":
    mode = os.getenv("RUN_MODE", "cli").strip().lower()

    if mode == "cli":
        run_cli()
    elif mode == "web":
        run_web()
    elif mode == "api":
        run_api()
    
    else:
        print(f"[Ошибка] Неизвестный режим: '{mode}'. Используйте 'cli' или 'web'.")
