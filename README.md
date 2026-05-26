```markdown
# Game Statistics Analyzer

The best ITP project — A Python application for analyzing game statistics with support for multiple data formats, built on Hexagonal Architecture principles.

## 🏗️ Hexagonal Architecture (Ports & Adapters)

This project fully implements Hexagonal Architecture to ensure complete isolation of business logic from external dependencies:

* `core/` - Domain layer with business logic (`GameRecord` model, `StatsAnalyzer` service)
* `ports/` - Abstract interfaces (ports) defining how the core communicates with the outside world
* `adapters/` - Concrete implementations (adapters) for:
  * **Storage:** JSON files, SQLite database
  * **User Interfaces:** CLI, Streamlit web app, FastAPI REST API
* `main.py` - Entry point for dependency injection and layer orchestration

This design allows you to change databases, add new UI frameworks, or modify data sources without touching the core business logic.

---

## ⚡ Core Features

* **O(n) metric calculation** - Efficient statistical analysis.
* **Streaming processing** - Handle large datasets via stream parsing and generators without memory issues.
* **Input validation** - Type checking and regex patterns for data integrity.
* **Advanced filtering** - SQLite queries for processing specific data subsets.
* **Decorator-based profiling** - `@time_it` decorator for algorithm performance measurement.

---

## 🚀 Running the Project

### Docker Compose
Run the full stack:
```bash
docker-compose up

```

Run FastAPI server only:

```bash
docker compose run --rm -p 8000:8000 game-analyzer uvicorn adapters.ui.fastapi_app:app --host 0.0.0.0 --port 8000

```

### Local Development

```bash
pip install -r requirements.txt
python main.py
streamlit run adapters/ui/streamlit_app.py

```

---

## 📊 Export & Data Formats

The application supports multiple data formats for both import and export.

### Export Capabilities

* **JSON:** Export statistics and analysis results to structured JSON files.
* **CSV:** Convert game records to CSV format for spreadsheet analysis.
* **SQLite:** Persistent storage with query support and data filtering.

### Data Sources

* **JSON files:** Stream parsing using generators (memory-efficient for large files).
* **SQLite databases:** Store and query game statistics with filtering capabilities.
* **In-memory processing:** For real-time analysis.

### Examples

#### JSON format

```json
{
  "total_games": 100,
  "average_score": 2450.5,
  "win_rate": 0.65,
  "top_scores": []
}

```

#### CSV format

```csv
player_name,game_date,score,game_mode
Player1,2026-05-20,3200,ranked
Player2,2026-05-20,1800,casual

```

---

## 🧪 Testing

To run the test suite, execute:

```bash
pytest tests/

```

---

## 🛠️ Requirements

* Python 3.8+
* Docker & Docker Compose
* Key dependencies: `Streamlit`, `FastAPI`, `Uvicorn`, `pytest`

---

## 👥 Contributors

* Zhylgeldi Bolat
* Ultradodoshka
* vitrimov
* ParasatAshk

```

```
