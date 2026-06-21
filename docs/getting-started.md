# Getting Started

## Requirements

- Python 3.12+
- [pipx](https://pipx.pypa.io/stable/) — for isolated CLI installation
- [Docker](https://docs.docker.com/get-docker/) — for services (Postgres, Kafka, etc.)

---

## Installation

```bash
pipx install degen-cli
```

Verify:

```bash
degen version
# degen 0.7.0
```

---

## Creating a project

Run `degen init` from any directory:

```bash
degen init
```

DEGEN will ask three questions:

```
Project name: my_pipeline

Select architecture pattern:
  ❯ Batch ETL
    Analytics
    Streaming

  [EXTRACT] Select tool:
  ❯ Python

  [TRANSFORM] Select tool:
  ❯ dbt

  [STORE] Select tool:
  ❯ DuckDB
```

After answering, DEGEN generates the project and shows what was created:

```
my_pipeline/
  .env
  Makefile
  degen.yaml
  docker-compose.yml
  profiles.yml
  requirements.txt
  data/raw/
    sample.csv
  src/
    extract.py

Next steps:
  cd my_pipeline
  degen install
  degen run
  degen seed
  degen test
  degen notebook
  degen docs
```

---

## Project commands

All commands run from inside the project directory.

```bash
cd my_pipeline
```

### Install dependencies

```bash
degen install
```

Creates a `.venv`, upgrades pip, installs `requirements.txt`, and runs any tool-specific setup (e.g. `dbt init`).

### Run the pipeline

```bash
degen run
```

Executes the pipeline end-to-end. For Batch ETL: extract → dbt run. For Analytics: Prefect/Airflow flow. For Streaming: starts the Kafka consumer.

### Check project status

```bash
degen status
```

Shows project info, available commands, web UI URLs, and Docker service health.

### List web UIs

```bash
degen ui
```

```
Tool              URL
Jupyter Lab       http://localhost:8888  (via: degen notebook)
dbt docs          http://localhost:8081  (via: degen docs)
```

---

## Project manifest — degen.yaml

Every project has a `degen.yaml` that defines the project and its commands:

```yaml
project: my_pipeline
pattern: Batch ETL
tools:
  - Python
  - dbt
  - DuckDB
ui:
  Jupyter Lab (DuckDB): http://localhost:8888
  dbt docs: http://localhost:8081
commands:
  install:
    steps:
      - python -m venv .venv
      - .venv/bin/pip install -r requirements.txt
  run:
    steps:
      - .venv/bin/python src/extract.py
      - cd my_pipeline && ../.venv/bin/dbt run --profiles-dir ..
```

You can add custom commands directly to `degen.yaml` and run them with:

```bash
degen exec <command-name>
```

---

## Updating the CLI

```bash
pipx upgrade degen
```
