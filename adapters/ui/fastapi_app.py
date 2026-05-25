import os

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, field_validator


from adapters.storage.json_storage import JSONFileAdapter
from core.models import DATE_PATTERN
from core.models import GameRecord
from core.services import StatsAnalyzer

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


_extra_records: list[GameRecord] = []


def _build_analyzer() -> StatsAnalyzer:
    file_path = os.getenv("DATA_FILE", "data/stats.json")
    file_adapter = JSONFileAdapter(file_path)

    def combined():
        yield from file_adapter.load_records()
        yield from _extra_records

    return StatsAnalyzer(combined())

app = FastAPI(
    title="Game Statistics Analyzer API",
    description="REST API для анализа игровой статистики",
    version="1.0.0",
)

@app.get("/leaderboard", response_model=list[LeaderboardEntry], tags=["analytics"])
def leaderboard():
    analyzer = _build_analyzer()
    return [
        LeaderboardEntry(player=player, best_score=score)
        for player, score in analyzer.get_leaderboard()
    ]


@app.get("/averages", response_model=list[AverageEntry], tags=["analytics"])
def averages():
    analyzer = _build_analyzer()
    return [
        AverageEntry(player=player, average_score=round(avg, 2))
        for player, avg in analyzer.get_average_scores()
    ]


@app.get("/records", response_model=RecordsResponse, tags=["analytics"])
def records():
    analyzer = _build_analyzer()
    data = analyzer.get_records()

    absolute = None
    if data["absolute_record"]:
        absolute = AbsoluteRecord(**data["absolute_record"])

    return RecordsResponse(
        absolute_record=absolute,
        daily_best=data["daily_best"],
    )

@app.post("/records", response_model=GameRecordInput, status_code=201, tags=["data"])
def add_record(record: GameRecordInput):
    try:
        game_record = GameRecord(
            player=record.player,
            score=record.score,
            date=record.date,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    _extra_records.append(game_record)
    return record


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}