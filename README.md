# game-statistics-analyzer

The best ITP project - A Python application for analyzing game statistics with support for multiple data formats, built on Hexagonal Architecture principles.

## Hexagonal Architecture (Ports & Adapters)

This project fully implements Hexagonal Architecture to ensure complete isolation of business logic from external dependencies:

- `core/` - Domain layer with business logic (`GameRecord` model, `StatsAnalyzer` service)
- `ports/` - Abstract interfaces (ports) defining how the core communicates with the outside world
- `adapters/` - Concrete implementations (adapters) for:
  - Storage: JSON files, SQLite database
  - User Interfaces: CLI, Streamlit web app, FastAPI REST API
- `main.py` - Entry point for dependency injection and layer orchestration

This design allows you to change databases, add new UI frameworks, or modify data sources without touching the core business logic.

## Running the Project

### Docker Compose

Full stack with Docker Compose:

```bash
docker-compose up

Run FastAPI server only:
bash

docker compose run --rm -p 8000:8000 game-analyzer uvicorn adapters.ui.fastapi_app:app --host 0.0.0.0 --port 8000

Local development:
bash

pip install -r requirements.txt
python main.py
streamlit run adapters/ui/streamlit_app.py

Export & Data Formats

The application supports multiple data formats for both import and export.
Export capabilities

    JSON - Export statistics and analysis results to structured JSON files

    CSV - Convert game records to CSV format for spreadsheet analysis

    SQLite - Persistent storage with query support and data filtering

Data sources

    JSON files - Stream parsing using generators (memory-efficient for large files)

    SQLite databases - Store and query game statistics with filtering capabilities

    In-memory processing - For real-time analysis

Example exports

JSON format:
json

{
  "total_games": 100,
  "average_score": 2450.5,
  "win_rate": 0.65,
  "top_scores": []
}

CSV format:
csv

player_name,game_date,score,game_mode
Player1,2026-05-20,3200,ranked
Player2,2026-05-20,1800,casual

Core Features

    O(n) metric calculation - Efficient statistical analysis

    Input validation - Type checking and regex patterns for data integrity

    Streaming processing - Handle large datasets without memory issues

    SQLite queries - Advanced filtering for specific data subsets

    Decorator-based profiling - @time_it decorator for algorithm performance measurement

Testing
bash

pytest tests/

Requirements

    Python 3.8+

    Docker & Docker Compose

    Streamlit, FastAPI, Uvicorn, pytest

Contributors

Zhylgeldi Bolat, Ultradodoshka, vitrimov, ParasatAshk
```text
game-statistics-analyzer/
│
├── .gitignore                # Конфигурация игнорируемых Git файлов и каталогов
├── Dockerfile                # Спецификация сборки контейнера и автоматического тестирования
├── README.md                 # Техническая документация проекта
├── main.py                   # Точка входа, оркестрация слоев и Dependency Injection
├── requirements.txt          # Декларация внешних зависимостей (Streamlit)
│
├── data/                     # Каталог локального хранения данных
│   ├── stats.json            # Тестовый набор данных в формате JSON для CLI-модуля
│   └── stats.db              # SQLite база данных с игровой статистикой
│
├── core/                     # Слой бизнес-логики (Доменная модель и сервисы)
│   ├── __init__.py
│   ├── models.py             # Сущность GameRecord, валидация типов и регулярных выражений
│   └── services.py           # StatsAnalyzer (Вычисление аналитических метрик за O(n))
│
├── ports/                    # Слой интерфейсов (Абстрактные контракты приложения)
│   ├── __init__.py
│   └── data_repository.py    # GameDataPort (Интерфейс для потокового чтения данных)
│
├── adapters/                 # Слой инфраструктуры (Реализация внешних интерфейсов)
│   ├── __init__.py
│   │
│   ├── storage/              # Компоненты работы с постоянным хранилищем
│   │   ├── json_storage.py   # JSONFileAdapter (Потоковый парсинг через генераторы)
│   │   └── sqlite_storage.py # SQLiteAdapter (Импорт JSON и хранение статистики в SQLite)
│   │
│   └── ui/                   # Компоненты пользовательского интерфейса
│       ├── cli_app.py        # CLIAdapter (Консольный вывод аналитических таблиц)
│       └── streamlit_app.py  # WebAdapter (Интерактивный веб-интерфейс и графики)
│
├── utils/                    # Слой вспомогательных утилит
│   ├── __init__.py
│   └── decorators.py         # Декоратор @time_it для профилирования скорости алгоритмов
│
└── tests/                    # Модульное тестирование приложения
    ├── __init__.py
    └── test_analyzer.py      # Набор Unit-тестов для верификации бизнес-логики
