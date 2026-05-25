import os

from adapters.storage.json_storage import JSONFileAdapter
from adapters.ui.cli_app import CLIAdapter
from core.services import StatsAnalyzer


def run_cli():
    file_path = os.getenv("DATA_FILE", "data/stats.json")

    print(f"[Загрузка] Читаем данные из: {file_path}")

    adapter = JSONFileAdapter(file_path)
    records = adapter.load_records()
    analyzer = StatsAnalyzer(records)

    cli = CLIAdapter(analyzer)
    cli.run()


def run_web():
    # Streamlit запускается отдельной командой, main.py только сообщает об этом
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
