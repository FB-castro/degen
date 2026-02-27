from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class Pattern(ABC):
    name: str
    supported_stacks: List[str] = []

    @abstractmethod
    def create_structure(self, root: Path):
        pass