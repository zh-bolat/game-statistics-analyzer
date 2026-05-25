from fastapi import FastAPI

app = FastAPI(
    title="Game Statistics Analyzer API",
    description="REST API для анализа игровой статистики",
    version="1.0.0",
)