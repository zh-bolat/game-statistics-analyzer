from collections import defaultdict
from typing import Generator

from core.models import GameRecord
from utils.decorators import time_it


class StatsAnalyzer:

    def init(self, records: Generator[GameRecord, None, None]):
        # Единственный проход по генератору — сохраняем данные в памяти
        self._records: list[GameRecord] = list(records)

    @time_it
    def get_leaderboard(self) -> list[tuple[str, int]]:
        """
        Глобальный лидерборд: максимальный счёт каждого игрока.
        Сложность: O(n)
        """
        best_scores: dict[str, int] = {}

        for record in self._records:
            if record.player not in best_scores:
                best_scores[record.player] = record.score
            elif record.score > best_scores[record.player]:
                best_scores[record.player] = record.score

        return sorted(best_scores.items(), key=lambda x: x[1], reverse=True)

    @time_it
    def get_average_scores(self) -> list[tuple[str, float]]:
        """
        Средний счёт каждого игрока по всем сессиям.
        Сложность: O(n)
        """
        totals: dict[str, int] = defaultdict(int)
        counts: dict[str, int] = defaultdict(int)

        for record in self._records:
            totals[record.player] += record.score
            counts[record.player] += 1

        averages = {
            player: totals[player] / counts[player]
            for player in totals
        }

        return sorted(averages.items(), key=lambda x: x[1], reverse=True)

    @time_it
    def get_records(self) -> dict:
        """
        Абсолютный рекорд за всё время и лучший результат по каждому дню.
        Сложность: O(n)
        """
        if not self._records:
            return {"all_
