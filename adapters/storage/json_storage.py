import json
from typing import Generator

from core.models import GameRecord
from ports.data_repository import GameDataPort


class JSONFileAdapter(GameDataPort):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def load_records(self) -> Generator[GameRecord, None, None]:

        with open(self._file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        for entry in raw_data:
            try:
                yield GameRecord(
                    player=entry["player"],
                    score=entry["score"],
                    date=entry["date"]
                )
            except (KeyError, ValueError, TypeError) as e:
                print(f"[Предупреждение] Запись пропущена: {entry} — Причина: {e}")
