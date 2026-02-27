from pathlib import Path
from degen.patterns.base import Pattern
from degen.registry.pattern_registry import PatternRegistry


class MedallionPattern(Pattern):
    name = "Medallion"
    supported_stacks = ["Spark + MinIO"]

    def create_structure(self, root: Path):
        (root / "src").mkdir(parents=True, exist_ok=True)
        (root / "lake/bronze").mkdir(parents=True, exist_ok=True)
        (root / "lake/silver").mkdir(parents=True, exist_ok=True)
        (root / "lake/gold").mkdir(parents=True, exist_ok=True)


PatternRegistry.register(MedallionPattern)