from pathlib import Path


def create_project_root(name: str) -> Path:
    """
    Cria o diretório raiz do projeto.
    """
    root = Path(name).resolve()

    if root.exists():
        raise FileExistsError(f"Directory '{name}' already exists.")

    root.mkdir(parents=True, exist_ok=False)

    return root


def create_common_files(root: Path, run_command: str = "python src/main.py"):
    """
    Cria arquivos base do projeto.
    """

    # Garantia extra de segurança
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

    # Makefile
    (root / "Makefile").write_text(
        f"""venv:
\tpython -m venv .venv

install: venv
\t. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
\t. .venv/bin/activate && {run_command}

docker-build:
\tdocker compose build

docker-up:
\tdocker compose up -d

docker-down:
\tdocker compose down
"""
    )