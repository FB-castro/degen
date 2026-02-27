from typing import Dict, Type
from degen.patterns.base import Pattern


class PatternRegistry:
    _patterns: Dict[str, Type[Pattern]] = {}

    @classmethod
    def register(cls, pattern: Type[Pattern]):
        cls._patterns[pattern.name] = pattern

    @classmethod
    def get(cls, name: str) -> Pattern:
        return cls._patterns[name]()

    @classmethod
    def list_patterns(cls):
        return list(cls._patterns.keys())