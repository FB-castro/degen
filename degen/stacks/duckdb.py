from pathlib import Path
from degen.stacks.base import Stack
from degen.registry.stack_registry import StackRegistry


class DuckDBStack(Stack):
    name = "DuckDB Local"

    def apply_stack(self, root: Path):

        # requirements
        (root / "requirements.txt").write_text(
            """duckdb==1.0.0
pandas==2.2.2
python-dotenv==1.0.1
"""
        )

        # .env
        (root / ".env").write_text(
            """DUCKDB_PATH=data/warehouse.duckdb
ENV=dev
"""
        )

        # Dockerfile
        (root / "Dockerfile").write_text(
            """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
"""
        )

        # docker-compose
        (root / "docker-compose.yml").write_text(
            """
services:
  app:
    build: .
    env_file:
      - .env
    volumes:
      - .:/app
"""
        )

        # Código mínimo funcional
        (root / "src/main.py").write_text(
            """import pandas as pd
import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

def run():
    df = pd.DataFrame({"id": [1,2], "name": ["Alice","Bob"]})
    df["name"] = df["name"].str.upper()

    con = duckdb.connect(os.getenv("DUCKDB_PATH"))
    con.execute("CREATE TABLE IF NOT EXISTS users AS SELECT * FROM df")

    print(con.execute("SELECT * FROM users").fetchall())

if __name__ == "__main__":
    run()
"""
        )


StackRegistry.register(DuckDBStack)