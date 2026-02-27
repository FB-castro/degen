from pathlib import Path


def create_common_files(root: Path, run_command: str = "python src/main.py"):

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

    (root / "Makefile").write_text(
        f"""venv:
\tpython -m venv .venv

install: venv
\t. .venv/bin/activate && pip install -r requirements.txt

run:
\t. .venv/bin/activate && {run_command}

docker-build:
\tdocker compose build

docker-up:
\tdocker compose up

docker-down:
\tdocker compose down
"""
    )