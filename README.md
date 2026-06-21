# DEGEN — Data Engineering Project Generator

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.7.1-brightgreen)

**Scaffold production-ready data pipelines in minutes, not hours.**

DEGEN is a CLI framework for data engineers. Answer three questions about your architecture, and DEGEN generates a complete, working project — Docker services, dependencies, configuration, pipeline scripts, and a unified `degen` command to run everything.

---

## Install

```bash
pipx install degen-cli
```

Requires Python 3.12+ and Docker.

---

## Quick start

```bash
degen init           # interactive project scaffold
cd my_project

degen install        # install dependencies
degen docker-up      # start services (Kafka, Postgres, etc.)
degen run            # execute the pipeline
degen ui             # list all web interfaces
degen status         # project health check
```

---

## Architecture Patterns

### Batch ETL

Extract data, transform with dbt, store in DuckDB or Postgres.

```bash
degen init           # select Batch ETL → Python + dbt + DuckDB
degen install
degen run            # extract → dbt run
degen seed           # load seed data
degen test           # dbt data quality tests
degen notebook       # Jupyter Lab at http://localhost:8888
degen docs           # dbt docs at http://localhost:8081
```

### Analytics

Orchestrate with Prefect or Airflow, visualize with Grafana or Metabase.

```bash
degen init           # select Analytics → Prefect + dbt + Postgres + Grafana
degen install
degen docker-up      # Postgres + pgAdmin + Grafana
degen prefect-server # Prefect UI at http://localhost:4200
degen run            # run Prefect flow
degen docs           # dbt docs at http://localhost:8081
```

### Streaming

Real-time event processing with Kafka and PySpark.

```bash
degen init           # select Streaming → Kafka + PySpark
degen install
degen docker-up      # Kafka + Kafka UI at http://localhost:8082
degen create-topic   # create Kafka topic
degen produce        # send 100 events to Kafka
degen stream         # PySpark consumer + Spark UI at http://localhost:4040
```

---

## Every tool has a web UI

| Tool | Interface | Port |
|---|---|---|
| Kafka | Kafka UI | :8082 |
| Postgres | pgAdmin 4 | :5050 |
| ClickHouse | ClickHouse Play | :8123/play |
| DuckDB | Jupyter Lab (`degen notebook`) | :8888 |
| dbt | dbt Docs (`degen docs`) | :8081 |
| PySpark | Spark UI (auto) | :4040 |
| Airflow | Airflow UI | :8080 |
| Prefect | Prefect UI | :4200 |
| Metabase | Metabase | :3000 |
| Grafana | Grafana | :3001 |

---

## What DEGEN generates

Every project includes:

```
my_project/
├── degen.yaml              # project manifest — pattern, tools, commands
├── docker-compose.yml      # all services, pre-wired and ready
├── requirements.txt        # pinned dependencies
├── .env                    # environment variables with sensible defaults
├── Makefile                # for CI/CD and power users
├── profiles.yml            # dbt connection config (when applicable)
├── src/
│   └── extract.py          # pipeline scripts
└── my_project/             # dbt project (when applicable)
    ├── dbt_project.yml
    └── models/
```

Every command you'd normally wire up manually — `python -m venv`, `pip install`, `dbt init`, `docker compose up`, `dbt run`, `jupyter lab` — becomes a single `degen` command with real-time Rich output.

---

## degen.yaml

The project manifest defines all available commands:

```yaml
project: my_project
pattern: Batch ETL
tools:
  - Python
  - dbt
  - DuckDB
ui:
  Jupyter Lab: http://localhost:8888
  dbt docs: http://localhost:8081
commands:
  install:
    steps:
      - python -m venv .venv
      - .venv/bin/pip install -r requirements.txt
      - .venv/bin/dbt init my_project --skip-profile-setup
  run:
    steps:
      - .venv/bin/python src/extract.py
      - cd my_project && ../.venv/bin/dbt run --profiles-dir ..
  seed:
    steps:
      - cd my_project && ../.venv/bin/dbt seed --profiles-dir ..
  test:
    steps:
      - cd my_project && ../.venv/bin/dbt test --profiles-dir ..
```

Add custom commands and run them with `degen exec <command>`.

---

## CLI reference

| Command | Description |
|---|---|
| `degen init` | Scaffold a new project interactively |
| `degen status` | Project health + available commands + UI URLs |
| `degen ui` | List all web interface URLs |
| `degen install` | Install dependencies |
| `degen docker-up` | Start Docker services |
| `degen docker-down` | Stop Docker services |
| `degen run` | Execute the pipeline end-to-end |
| `degen stream` | Start PySpark streaming consumer |
| `degen produce` | Send 100 synthetic events to Kafka |
| `degen create-topic` | Create Kafka topic |
| `degen seed` | Load dbt seed data |
| `degen test` | Run dbt tests |
| `degen docs` | Serve dbt documentation |
| `degen notebook` | Start Jupyter Lab |
| `degen prefect-server` | Start Prefect backend |
| `degen exec <cmd>` | Run any custom command from degen.yaml |
| `degen version` | Print installed version |

---

## Supported tools

| Phase | Tools |
|---|---|
| Extract | Python (pandas + requests) |
| Transform | dbt · PySpark |
| Store | DuckDB · Postgres · ClickHouse |
| Orchestrate | Prefect · Airflow |
| Serve | Grafana · Metabase |
| Stream | Kafka (KRaft, no Zookeeper) |

All tools are 100% open source.

---

## Design philosophy

- **Opinionated**: clear defaults, no analysis paralysis
- **Complete**: every tool comes with Docker, config, UI, and a `degen` command
- **Practical**: generates working code you can run immediately and customize from there
- **Open source only**: every dependency is freely available and self-hostable

---

## Documentation

Full hands-on guides at the documentation site:

- [Getting Started](https://fb-castro.github.io/degen/getting-started/)
- [Batch ETL](https://fb-castro.github.io/degen/patterns/batch-etl/)
- [Analytics](https://fb-castro.github.io/degen/patterns/analytics/)
- [Streaming](https://fb-castro.github.io/degen/patterns/streaming/)
- [CLI Reference](https://fb-castro.github.io/degen/cli-reference/)

---

## Development

```bash
git clone https://github.com/FB-castro/degen.git
cd degen
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## License

MIT
