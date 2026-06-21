# 1. Init & Install

In this step you'll scaffold the project and install all dependencies.

---

## Create the project

Run `degen init` from any directory:

```bash
degen init
```

Answer the prompts as shown below:

```
Project name: sales_pipeline

Select architecture pattern:
  ❯ Analytics

  [ORCHESTRATE] Select tool:
  ❯ Airflow

  [TRANSFORM] Select tool:
  ❯ dbt

  [STORE] Select tool:
  ❯ Postgres

  [SERVE] Select tool:
  ❯ Grafana
```

DEGEN generates the project and shows the file tree:

```
sales_pipeline/
  .env
  Makefile
  degen.yaml
  docker-compose.yml
  profiles.yml
  requirements.txt
  dags/
    pipeline_dag.py
  src/
    extract.py

Next steps:
  cd sales_pipeline
  degen install
  degen docker-up
  degen run
```

Enter the project directory:

```bash
cd sales_pipeline
```

---

## Install dependencies

```bash
degen install
```

This creates `.venv`, installs all Python packages, and scaffolds the dbt project:

```
degen install
─────────────
$ python -m venv .venv
$ .venv/bin/pip install --upgrade pip
$ .venv/bin/pip install -r requirements.txt
...
Successfully installed apache-airflow dbt-core dbt-postgres pyspark psycopg2-binary

$ .venv/bin/dbt init sales_pipeline --skip-profile-setup
Your new dbt project "sales_pipeline" was created!
✓ Done
```

---

## What was generated

Open `degen.yaml` to see all available commands:

```yaml title="degen.yaml"
project: sales_pipeline
pattern: Analytics
tools:
  - Airflow
  - dbt
  - Postgres
  - Grafana
ui:
  Airflow UI: http://localhost:8080
  pgAdmin: http://localhost:5050
  Grafana: http://localhost:3001
  dbt docs: http://localhost:8081
commands:
  install:
    steps:
      - python -m venv .venv
      - .venv/bin/pip install -r requirements.txt
      - .venv/bin/dbt init sales_pipeline --skip-profile-setup
  docker-up:
    steps:
      - docker compose up -d
  run:
    steps:
      - .venv/bin/python src/extract.py
  ...
```

The `profiles.yml` has the Postgres connection already configured using dbt's `env_var()` syntax — it reads from `.env` automatically:

```yaml title="profiles.yml"
sales_pipeline:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('POSTGRES_HOST', 'localhost') }}"
      port: 5432
      user: "{{ env_var('POSTGRES_USER', 'degen') }}"
      password: "{{ env_var('POSTGRES_PASSWORD', 'degen') }}"
      dbname: "{{ env_var('POSTGRES_DB', 'degen') }}"
      schema: public
      threads: 4
```

---

## Check project status

```bash
degen status
```

```
Project:   sales_pipeline
Pattern:   Analytics

Available commands:
  degen install       install dependencies
  degen docker-up     start Docker services
  degen docker-down   stop Docker services
  degen run           execute pipeline
  degen docs          serve dbt docs at :8081

Web UIs:
  Airflow UI    http://localhost:8080   (via: degen docker-up)
  pgAdmin       http://localhost:5050   (via: degen docker-up)
  Grafana       http://localhost:3001   (via: degen docker-up)
  dbt docs      http://localhost:8081   (via: degen docs)

Docker services:
  Not running. Run: degen docker-up
```

[Next: Start Services →](02-docker.md){ .md-button .md-button--primary }
