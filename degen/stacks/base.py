from abc import ABC, abstractmethod
from pathlib import Path


class Stack(ABC):
    name: str

    @abstractmethod
    def apply_stack(self, root: Path):
        pass