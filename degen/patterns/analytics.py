from pathlib import Path
from degen.patterns.base import Pattern
from degen.registry.pattern_registry import PatternRegistry


class AnalyticsPattern(Pattern):
    name = "Analytics"
    supported_stacks = ["dbt + DuckDB"]

    def create_structure(self, root: Path):
        (root / "models").mkdir(parents=True, exist_ok=True)
        (root / "data").mkdir(parents=True, exist_ok=True)


PatternRegistry.register(AnalyticsPattern)