from pathlib import Path
from degen.registry.pattern_registry import PatternRegistry
from degen.registry.stack_registry import StackRegistry
from degen.core.project_scaffold import create_common_files
from degen.core.logger import logger

def generate_project(project_name: str, pattern_name: str, stack_name: str):
    logger.debug(f"Generating project at {root}")
    logger.debug(f"Applying pattern: {pattern_name}")
    logger.debug(f"Applying stack: {stack_name}")
    root = Path.cwd() / project_name
    root.mkdir(parents=True, exist_ok=True)

    pattern = PatternRegistry.get(pattern_name)

    if stack_name not in pattern.supported_stacks:
        raise ValueError(
            f"Stack '{stack_name}' não é compatível com Pattern '{pattern_name}'"
        )

    stack = StackRegistry.get(stack_name)

    pattern.create_structure(root)

    # Definir run command por stack
    run_map = {
        "DuckDB Local": "python src/main.py",
        "Spark + MinIO": "python src/pipeline.py",
        "Airflow + Postgres": "airflow standalone",
        "dbt + DuckDB": "export DBT_PROFILES_DIR=. && dbt run",
    }

    run_command = run_map.get(stack_name, "python src/main.py")

    create_common_files(root, run_command=run_command)

    stack.apply_stack(root)