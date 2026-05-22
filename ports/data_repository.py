from abc import ABC, abstractmethod
from typing import Generator
from core.models import GameRecord


class GameDataPort(ABC):

    @abstractmethod
    def load_records(self) -> Generator[GameRecord, None, None]:
        raise NotImplementedError