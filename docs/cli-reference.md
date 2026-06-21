# CLI Reference

All `degen` commands run from within a project directory (where `degen.yaml` lives).

---

## Global commands

These work from any directory.

### `degen init`

Scaffold a new data engineering project interactively.

```bash
degen init
```

Asks for: project name, architecture pattern, tool selection per phase.

Generates: `degen.yaml`, `docker-compose.yml`, `requirements.txt`, `.env`, `Makefile`, pipeline scripts.

---

### `degen version`

Print the installed version.

```bash
degen version
# degen 0.7.0
```

---

## Project commands

Run from inside a project directory (or any subdirectory — DEGEN walks up to find `degen.yaml`).

---

### `degen status`

Show project health at a glance.

```bash
degen status
```

Output includes:

- Project name and pattern
- All available commands for this pattern
- Web UI URLs and how to launch them
- Docker service health (if services are running)

---

### `degen ui`

List all web interfaces available for this project.

```bash
degen ui
```

```
Tool              URL
────────────────────────────────────────
Kafka UI          http://localhost:8082
Prefect UI        http://localhost:4200
Grafana           http://localhost:3001
pgAdmin           http://localhost:5050
```

---

### `degen install`

Install project dependencies.

```bash
degen install
```

- Creates `.venv`
- Installs `requirements.txt` via pip
- Runs tool-specific setup (e.g. `dbt init`)

---

### `degen docker-up`

Start Docker services defined in `docker-compose.yml`.

```bash
degen docker-up
```

Equivalent to `docker compose up -d`.

---

### `degen docker-down`

Stop and remove Docker containers.

```bash
degen docker-down
```

Data volumes are preserved. To remove volumes: `docker compose down -v`.

---

### `degen run`

Execute the pipeline end-to-end.

```bash
degen run
```

| Pattern | What runs |
|---|---|
| Batch ETL | `extract.py` → `dbt run` |
| Analytics | Prefect/Airflow flow |
| Streaming | Kafka consumer (Ctrl+C to stop) |

---

### `degen stream`

Start the PySpark Structured Streaming consumer. **Streaming pattern only.**

```bash
degen stream
```

Reads from Kafka and prints micro-batches to the console. Runs until `Ctrl+C`.

---

### `degen produce`

Send 100 synthetic events to Kafka. **Streaming pattern only.**

```bash
degen produce
```

---

### `degen create-topic`

Create the Kafka topic from `.env`. **Streaming pattern only.**

```bash
degen create-topic
```

---

### `degen seed`

Load dbt seed CSV files into the database.

```bash
degen seed
```

Runs `dbt seed` using the project's `profiles.yml`.

---

### `degen test`

Run dbt data quality tests.

```bash
degen test
```

Runs `dbt test` and reports PASS/FAIL for each test.

---

### `degen docs`

Generate and serve dbt documentation.

```bash
degen docs
```

Runs `dbt docs generate` then `dbt docs serve` at **http://localhost:8081**.

Press `Ctrl+C` to stop.

---

### `degen notebook`

Start Jupyter Lab.

```bash
degen notebook
```

Opens Jupyter Lab at **http://localhost:8888**.

!!! tip
    For DuckDB projects, always use `read_only=True` when connecting from a notebook if `degen run` may be running concurrently.

---

### `degen prefect-server`

Start the Prefect backend server. **Analytics pattern (Prefect) only.**

```bash
degen prefect-server
```

Opens Prefect UI at **http://localhost:4200**. Runs until `Ctrl+C`.

---

### `degen orchestrate`

Print the orchestrator UI URL for this project.

```bash
degen orchestrate
```

---

### `degen serve`

Start the data serving layer (e.g. Metabase).

```bash
degen serve
```

---

### `degen exec <command>`

Run any custom command defined in `degen.yaml`.

```bash
degen exec my-command
```

Use this to extend DEGEN with your own pipeline steps.

---

## Adding custom commands

Edit `degen.yaml` to add commands:

```yaml
commands:
  load-raw:
    steps:
      - .venv/bin/python src/load_raw.py
  full-refresh:
    deps:
      - load-raw
    steps:
      - cd my_project && ../.venv/bin/dbt run --full-refresh --profiles-dir ..
```

Run them:

```bash
degen exec load-raw
degen exec full-refresh   # runs load-raw first, then dbt
```

---

## Environment variables

All commands inherit the environment and load `.env` automatically.

```bash
# .env
POSTGRES_HOST=localhost
POSTGRES_USER=degen
POSTGRES_PASSWORD=degen
POSTGRES_DB=degen
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=degen-events
```

Override any variable inline:

```bash
KAFKA_TOPIC=my-topic degen produce
```
