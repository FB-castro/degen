# Analytics

Orchestrate pipelines with Prefect or Airflow, transform data with dbt, and visualize results with Grafana or Metabase.

**Best for:** scheduled workflows with monitoring, BI dashboards, data observability.

---

## Tools

| Phase | Options |
|---|---|
| Orchestrate | Prefect · Airflow |
| Transform | dbt |
| Store | Postgres · ClickHouse |
| Serve | Grafana · Metabase |

---

## Create the project

```bash
degen init
```

Select **Analytics**. This guide uses **Prefect + dbt + Postgres + Grafana**.

```bash
cd my_analytics_project
```

---

## Install

```bash
degen install
```

Installs: prefect, dbt-core, dbt-postgres, psycopg2-binary, and scaffolds the dbt project.

---

## Start services

```bash
degen docker-up
```

Starts three containers:

| Container | Service | Port |
|---|---|---|
| `degen_postgres` | PostgreSQL 16 | 5432 |
| `degen_pgadmin` | pgAdmin 4 | 5050 |
| `degen_grafana` | Grafana | 3001 |

Wait ~10 seconds for all services to become healthy:

```bash
degen status
```

```
Docker services:
NAME              STATUS
degen_postgres    Up (healthy)
degen_pgadmin     Up
degen_grafana     Up (healthy)
```

---

## Start Prefect server

Open a dedicated terminal and run:

```bash
degen prefect-server
```

This starts the Prefect backend. Navigate to **http://localhost:4200** to open the Prefect UI.

---

## Run the pipeline

In another terminal:

```bash
degen run
```

The Prefect flow runs three tasks in sequence:

```
INFO  Flow run 'bold-falcon' - Beginning flow run for flow 'degen-pipeline'
INFO  Task run 'extract-812' - Extracting data... Extracted 5 records
INFO  Task run 'transform-42c' - Transforming data... Transformed 5 records
INFO  Task run 'load-fd1' - Loading data... Load complete.
INFO  Flow run 'bold-falcon' - Finished in state Completed()
```

---

## Validate in Prefect UI

Open **http://localhost:4200**

- **Flow Runs** → see all executions with timing and status
- **Flows** → registered flows
- **Tasks** → individual task runs with logs

Each run shows the full execution tree: `extract → transform → load`

---

## pgAdmin — browse Postgres

Open **http://localhost:5050**

| Field | Value |
|---|---|
| Login | `admin@degen.io` |
| Password | `degen` |

The server **"DEGEN Postgres"** is pre-configured. Click it and enter the database password:

| Field | Value |
|---|---|
| Password | `degen` |

Navigate to: **Servers → DEGEN Postgres → Databases → degen → Schemas → public → Tables**

---

## Grafana — build dashboards

Open **http://localhost:3001**

| Field | Value |
|---|---|
| Login | `admin` |
| Password | `admin` |

Add Postgres as a data source:

1. **Connections → Data Sources → Add → PostgreSQL**
2. Fill in:

| Field | Value |
|---|---|
| Host | `postgres:5432` |
| Database | `degen` |
| User | `degen` |
| Password | `degen` |
| TLS/SSL | Disable |

3. Click **Save & Test**
4. Create dashboards with SQL queries against your dbt models

---

## dbt documentation

```bash
degen docs
```

Serves the dbt lineage graph and model docs at **http://localhost:8081**.

---

## Using Airflow instead of Prefect

Select **Airflow** during `degen init`. DEGEN configures 4 containers:

| Container | Role |
|---|---|
| `airflow-postgres` | Airflow metadata DB |
| `airflow-init` | DB migration + admin user |
| `airflow-webserver` | UI at :8080 (admin/admin) |
| `airflow-scheduler` | DAG scheduler |

```bash
degen docker-up       # starts all 4 Airflow services
degen orchestrate     # prints Airflow UI URL
```

A sample DAG with `extract → transform` tasks is pre-generated in `dags/pipeline_dag.py`.

---

## Project structure

```
my_analytics_project/
├── degen.yaml
├── .env
├── profiles.yml            # Postgres connection with env_var()
├── docker-compose.yml      # Postgres + pgAdmin + Grafana
├── requirements.txt
├── flows/
│   └── pipeline_flow.py    # Prefect flow (or dags/ for Airflow)
└── my_analytics_project/   # dbt project
    ├── dbt_project.yml
    └── models/
```
