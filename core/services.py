from collections import defaultdict
from typing import Generator

from core.models import GameRecord
from utils.decorators import time_it


class StatsAnalyzer:

    def __init__(self, records: Generator[GameRecord, None, None]):
        self._best_scores: dict[str, int] = {}
        self._totals: dict[str, int] = defaultdict(int)
        self._counts: dict[str, int] = defaultdict(int)
        
        self._absolute_record_score = -1
        self._absolute_record_holder = None
        self._daily_best: dict[str, int] = {}

        for record in records:
            if record.player not in self._best_scores or record.score > self._best_scores[record.player]:
                self._best_scores[record.player] = record.score

            self._totals[record.player] += record.score
            self._counts[record.player] += 1

            if record.score > self._absolute_record_score:
                self._absolute_record_score = record.score
                self._absolute_record_holder = record.player
                
            if record.date not in self._daily_best or record.score > self._daily_best[record.date]:
                self._daily_best[record.date] = record.score

    @time_it
    def get_leaderboard(self) -> list[tuple[str, int]]:
        return sorted(self._best_scores.items(), key=lambda x: x[1], reverse=True)

    @time_it
    def get_average_scores(self) -> list[tuple[str, float]]:
        averages = {
            player: self._totals[player] / self._counts[player]
            for player in self._totals
        }
        return sorted(averages.items(), key=lambda x: x[1], reverse=True)

    @time_it
    def get_records(self) -> dict:
        if not self._best_scores:
            return {
                "absolute_record": None,
                "daily_best": {}
            }

        return {
            "absolute_record": {
                "player": self._absolute_record_holder,
                "score": self._absolute_record_score
            },
            "daily_best": self._daily_best
        }
