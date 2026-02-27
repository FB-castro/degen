from pathlib import Path
from degen.stacks.base import Stack
from degen.registry.stack_registry import StackRegistry


class DBTStack(Stack):
    name = "dbt + DuckDB"

    def apply_stack(self, root: Path):

        (root / "requirements.txt").write_text(
            """dbt-core==1.7.14
dbt-duckdb==1.7.2
"""
        )

        (root / ".env").write_text("ENV=dev\n")

        (root / "profiles.yml").write_text(
            """default:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: data/warehouse.duckdb
      threads: 1
"""
        )

        (root / "dbt_project.yml").write_text(
            f"""name: {root.name}
version: 1.0
profile: default

models:
  {root.name}:
    +materialized: table
"""
        )

        models_dir = root / "models"
        models_dir.mkdir(parents=True, exist_ok=True)

        (models_dir / "example.sql").write_text(
            "select 1 as id, 'degen' as name\n"
        )


StackRegistry.register(DBTStack)