# 2. Start Services

In this step you'll bring up all Docker containers and verify they're healthy.

---

## Start Docker

```bash
degen docker-up
```

This runs `docker compose up -d` using the generated `docker-compose.yml`.

```
degen docker-up
───────────────
$ docker compose up -d
[+] Running 6/6
 ✔ Network sales_pipeline_default    Created
 ✔ Container sales_pipeline_postgres Started
 ✔ Container sales_pipeline_pgadmin  Started
 ✔ Container sales_pipeline_grafana  Started
 ✔ Container airflow-init            Started
 ✔ Container airflow-webserver       Started
 ✔ Container airflow-scheduler       Started
✓ Done
```

Wait about 30 seconds for Airflow to finish its database migration, then check status:

```bash
degen status
```

```
Docker services:
NAME                          STATUS
sales_pipeline_postgres       Up (healthy)
sales_pipeline_pgadmin        Up
sales_pipeline_grafana        Up (healthy)
airflow-webserver             Up (healthy)
airflow-scheduler             Up
```

---

## Open the UIs

All three UIs are available immediately.

### Airflow — http://localhost:8080

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin` |

You'll see the DAGs list. It's empty for now — you'll add the pipeline DAG in the next step.

### pgAdmin — http://localhost:5050

| Field | Value |
|---|---|
| Email | `admin@degen.io` |
| Password | `degen` |

The server **"DEGEN Postgres"** is pre-registered. Click it, enter the database password `degen`, and you'll see the `degen` database ready.

### Grafana — http://localhost:3001

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin` |

Grafana is up. You'll configure a data source and dashboard in step 6.

---

## Inspect the docker-compose.yml

The generated file wires everything together. Key sections:

```yaml title="docker-compose.yml"
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-degen}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-degen}
      POSTGRES_DB: ${POSTGRES_DB:-degen}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "degen"]

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@degen.io
      PGADMIN_DEFAULT_PASSWORD: degen
      PGADMIN_SERVER_JSON_FILE: /pgadmin4/servers.json
    ports:
      - "5050:80"

  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    ports:
      - "3001:3000"

  airflow-webserver:
    image: apache/airflow:2.9.1
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://degen:degen@postgres/degen
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
    depends_on:
      postgres:
        condition: service_healthy
```

!!! tip
    The `dags/` folder is volume-mounted into Airflow. Any file you create there appears in the Airflow UI within 30 seconds — no restart needed.

[Next: Create the DAG →](03-airflow-dag.md){ .md-button .md-button--primary }
