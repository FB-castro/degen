# DEGEN — Data Engineering Project Generator

**Scaffold production-ready data pipelines in minutes, not hours.**

DEGEN is a CLI framework for data engineers. Choose your architecture pattern and tools interactively — DEGEN generates a complete, working project with Docker services, dependencies, configuration, and a dedicated CLI to run everything.

---

## Install

```bash
pipx install degen
```

---

## Create your first project

```bash
degen init
```

Answer three questions. DEGEN generates everything else.

```bash
cd my_project
degen install    # install dependencies
degen docker-up  # start services
degen run        # execute the pipeline
degen ui         # see all web interfaces
degen status     # project health check
```

---

## Architecture Patterns

Choose the pattern that fits your use case:

<div class="grid cards" markdown>

-   **Batch ETL**

    ---

    Extract data from sources, transform with dbt, store in DuckDB or Postgres.

    Tools: Python · dbt · DuckDB · Postgres

    [:octicons-arrow-right-24: Batch ETL guide](patterns/batch-etl.md)

-   **Analytics**

    ---

    Orchestrate pipelines with Prefect or Airflow, visualize with Grafana or Metabase.

    Tools: Prefect · Airflow · dbt · Postgres · Grafana · Metabase

    [:octicons-arrow-right-24: Analytics guide](patterns/analytics.md)

-   **Streaming**

    ---

    Real-time event processing with Kafka and PySpark Structured Streaming.

    Tools: Kafka · PySpark · ClickHouse

    [:octicons-arrow-right-24: Streaming guide](patterns/streaming.md)

</div>

---

## What DEGEN generates

Every project includes:

| File | Description |
|---|---|
| `degen.yaml` | Project manifest — pattern, tools, commands |
| `docker-compose.yml` | All services pre-configured and wired |
| `requirements.txt` | Exact pinned dependencies |
| `.env` | Environment variables with sensible defaults |
| `Makefile` | Fallback for CI/CD and power users |
| `profiles.yml` | dbt connection profile (when applicable) |
| `src/` | Ready-to-run pipeline scripts |

---

## Tools available

| Phase | Tools |
|---|---|
| Extract | Python (pandas + requests) |
| Transform | dbt · PySpark |
| Store | DuckDB · Postgres · ClickHouse |
| Orchestrate | Prefect · Airflow |
| Serve | Grafana · Metabase |
| Stream | Kafka |

---

## Every tool has a web UI

| Tool | UI | Port |
|---|---|---|
| Kafka | Kafka UI | :8082 |
| Postgres | pgAdmin 4 | :5050 |
| ClickHouse | ClickHouse Play (built-in) | :8123/play |
| DuckDB | Jupyter Lab (`degen notebook`) | :8888 |
| dbt | dbt Docs (`degen docs`) | :8081 |
| PySpark | Spark UI (auto) | :4040 |
| Airflow | Airflow UI | :8080 |
| Prefect | Prefect UI | :4200 |
| Metabase | Metabase | :3000 |
| Grafana | Grafana | :3001 |
