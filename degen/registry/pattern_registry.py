from typing import Dict, Type, List
from degen.patterns.base import Pattern


class PatternRegistry:
    _patterns: Dict[str, Type[Pattern]] = {}

    @classmethod
    def register(cls, pattern: Type[Pattern]) -> None:
        cls._patterns[pattern.name] = pattern

    @classmethod
    def get(cls, name: str) -> Pattern:
        if name not in cls._patterns:
            available = ", ".join(cls._patterns.keys()) or "none"
            raise ValueError(
                f"Pattern '{name}' não encontrado. Disponíveis: {available}"
            )
        return cls._patterns[name]()

    @classmethod
    def list_patterns(cls) -> List[str]:
        return list(cls._patterns.keys())

    @classmethod
    def exists(cls, name: str) -> bool:
        return name in cls._patterns