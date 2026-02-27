from pathlib import Path
from degen.patterns.base import Pattern
from degen.registry.pattern_registry import PatternRegistry


class BatchPattern(Pattern):
    name = "Batch ETL"
    supported_stacks = ["DuckDB Local", "dbt + DuckDB"]

    def create_structure(self, root: Path):
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "data/raw").mkdir(parents=True, exist_ok=True)
        (root / "data/processed").mkdir(parents=True, exist_ok=True)


PatternRegistry.register(BatchPattern)