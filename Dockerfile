FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Автоматический прогон тестов при сборке образа
# Если тесты упадут — образ не соберётся
RUN python -m unittest discover -s tests -v

ENV RUN_MODE=web
ENV DATA_FILE=data/stats.json

EXPOSE 8501

CMD ["streamlit", "run", "adapters/ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
