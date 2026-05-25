import re
from dataclasses import dataclass

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class GameRecord:
    player: str
    score: int
    date: str

    def __post_init__(self):
        if not isinstance(self.player, str) or not self.player.strip():
            raise ValueError(f"Некорректное имя игрока: '{self.player}'")

        if (
            not isinstance(self.score, int)
            or isinstance(self.score, bool)
            or self.score < 0
        ):
            raise ValueError(f"Некорректный счёт: '{self.score}'")

        if not isinstance(self.date, str) or not DATE_PATTERN.match(self.date):
            raise ValueError(
                f"Некорректный формат даты: '{self.date}'. Ожидается YYYY-MM-DD"
            )
