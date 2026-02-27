from pathlib import Path
from degen.patterns.base import Pattern
from degen.registry.pattern_registry import PatternRegistry


class ELTPattern(Pattern):
    name = "ELT"
    supported_stacks = ["Airflow + Postgres"]

    def create_structure(self, root: Path):
        (root / "dags").mkdir(parents=True, exist_ok=True)
        (root / "logs").mkdir(parents=True, exist_ok=True)
        (root / "plugins").mkdir(parents=True, exist_ok=True)
        (root / "src").mkdir(parents=True, exist_ok=True)


PatternRegistry.register(ELTPattern)