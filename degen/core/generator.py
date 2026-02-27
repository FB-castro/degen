from pathlib import Path

from degen.registry.pattern_registry import PatternRegistry
from degen.registry.stack_registry import StackRegistry
from degen.core.project_scaffold import create_common_files
from degen.core.logger import logger


def generate_project(project_name: str, pattern_name: str, stack_name: str):
    """
    Gera um novo projeto baseado em Pattern + Stack.
    """

    # 1️⃣ Definir root corretamente
    root = Path.cwd() / project_name

    logger.debug(f"Generating project at {root}")
    logger.debug(f"Applying pattern: {pattern_name}")
    logger.debug(f"Applying stack: {stack_name}")

    # 2️⃣ Falhar se diretório já existir
    if root.exists():
        raise FileExistsError(f"Directory '{project_name}' already exists.")

    root.mkdir(parents=True, exist_ok=False)

    # 3️⃣ Resolver Pattern
    pattern = PatternRegistry.get(pattern_name)

    if pattern is None:
        raise ValueError(f"Pattern '{pattern_name}' não encontrado.")

    # 4️⃣ Validar compatibilidade stack
    if stack_name not in pattern.supported_stacks:
        raise ValueError(
            f"Stack '{stack_name}' não é compatível com Pattern '{pattern_name}'"
        )

    # 5️⃣ Resolver Stack
    stack = StackRegistry.get(stack_name)

    if stack is None:
        raise ValueError(f"Stack '{stack_name}' não encontrada.")

    # 6️⃣ Criar estrutura base do pattern
    pattern.create_structure(root)

    # 7️⃣ Aplicar stack
    stack.apply_stack(root)

    # 8️⃣ Definir comando de execução por stack
    run_map = {
        "DuckDB Local": "python src/main.py",
        "Spark + MinIO": "python src/pipeline.py",
        "Airflow + Postgres": "airflow standalone",
        "dbt + DuckDB": "export DBT_PROFILES_DIR=. && dbt run",
    }

    run_command = run_map.get(stack_name, "python src/main.py")

    # 9️⃣ Criar arquivos comuns (Makefile, gitignore)
    create_common_files(root, run_command=run_command)

    logger.info(f"Project '{project_name}' successfully generated.")