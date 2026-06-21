from pathlib import Path
import yaml

DEGEN_FILE = "degen.yaml"


class ProjectConfig:
    def __init__(self, data: dict, root: Path):
        self.project = data["project"]
        self.pattern = data["pattern"]
        self.tools = data.get("tools", [])
        self.ui = data.get("ui", {})
        self.commands = data.get("commands", {})
        self.root = root

    def has_command(self, name: str) -> bool:
        return name in self.commands

    def available_commands(self) -> list[str]:
        return list(self.commands.keys())


def load_config() -> ProjectConfig:
    root = _find_root()
    if root is None:
        raise SystemExit(
            "Not a degen project. Navigate to a project directory or run 'degen init'."
        )
    data = yaml.safe_load((root / DEGEN_FILE).read_text())
    return ProjectConfig(data, root)


def _find_root() -> Path | None:
    for parent in [Path.cwd(), *Path.cwd().parents]:
        if (parent / DEGEN_FILE).exists():
            return parent
    return None
