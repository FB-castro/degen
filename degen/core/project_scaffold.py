from pathlib import Path


def create_common_files(root: Path, run_command: str = "python src/main.py"):
    """
    Cria arquivos base do projeto.
    """

    root.mkdir(parents=True, exist_ok=True)

    # .gitignore
    (root / ".gitignore").write_text(
        """.venv
__pycache__
*.pyc
.env
.env.*
.DS_Store
lake/
data/
logs/
"""
    )

    # Makefile otimizado para CI
    (root / "Makefile").write_text(
        f"""venv:
\tpython -m venv .venv

install: venv
\t. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
\t. .venv/bin/activate && {run_command}

docker-build:
\t@if [ -f docker-compose.yml ]; then docker compose build; else echo "No docker-compose.yml, skipping build"; fi

docker-up:
\t@if [ -f docker-compose.yml ]; then docker compose up -d; else echo "No docker-compose.yml, skipping docker-up"; fi

docker-down:
\t@if [ -f docker-compose.yml ]; then docker compose down; else echo "No docker-compose.yml, skipping docker-down"; fi

docker-validate:
\t@if [ -f docker-compose.yml ]; then docker compose config > /dev/null; else echo "No docker-compose.yml, skipping validation"; fi
"""
    )