from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from core.models import DATE_PATTERN

class GameRecordInput(BaseModel):
    player: str
    score: int
    date: str

    @field_validator("player")
    @classmethod
    def player_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Имя игрока не может быть пустым")
        return v

    @field_validator("score")
    @classmethod
    def score_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Счёт должен быть >= 0")
        return v

    @field_validator("date")
    @classmethod
    def date_format(cls, v: str) -> str:
        if not DATE_PATTERN.match(v):
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")
        return v


class LeaderboardEntry(BaseModel):
    player: str
    best_score: int


class AverageEntry(BaseModel):
    player: str
    average_score: float


class AbsoluteRecord(BaseModel):
    player: str
    score: int


class RecordsResponse(BaseModel):
    absolute_record: AbsoluteRecord | None
    daily_best: dict[str, int]


app = FastAPI(
    title="Game Statistics Analyzer API",
    description="REST API для анализа игровой статистики",
    version="1.0.0",
)