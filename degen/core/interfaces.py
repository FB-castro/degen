from abc import ABC, abstractmethod
from pathlib import Path

class Pattern(ABC):
    @abstractmethod
    def create_structure(self, root: Path):
        pass

class Stack(ABC):
    @abstractmethod
    def apply_stack(self, root: Path):
        pass