# Tutorial: Airflow + PySpark + dbt

You'll build a complete Analytics pipeline from scratch. By the end you'll have:

- **Airflow** scheduling and running your pipeline
- **PySpark** transforming raw sales data
- **dbt** creating clean analytical models
- **Postgres** storing everything
- **pgAdmin** and **Grafana** for visual inspection

The tutorial has 6 short steps. Each one adds one piece to the puzzle.

---

## What you'll build

A sales data pipeline that:

1. Extracts synthetic daily sales records
2. Cleans and aggregates them with PySpark
3. Creates a `sales_summary` mart with dbt
4. Runs automatically via Airflow on a daily schedule
5. Exposes results in Grafana dashboards

```
raw_sales.csv  →  PySpark clean  →  Postgres (staging)
                                           ↓
                                    dbt run  →  sales_summary
                                           ↓
                                        Grafana
```

---

## Prerequisites

- Python 3.12+
- [pipx](https://pipx.pypa.io/stable/)
- [Docker Desktop](https://docs.docker.com/get-docker/) running

Install DEGEN:

```bash
pipx install degen
degen version   # degen 0.7.0
```

---

## Steps

<div class="feature-grid">
  <a href="01-init.md" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">1</span>
    <h3>Init & Install</h3>
    <p>Scaffold the project and install dependencies.</p>
  </a>
  <a href="02-docker/" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">2</span>
    <h3>Start Services</h3>
    <p>Launch Postgres, pgAdmin, Grafana, and Airflow.</p>
  </a>
  <a href="03-airflow-dag/" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">3</span>
    <h3>Create the DAG</h3>
    <p>Write the Airflow DAG that orchestrates the pipeline.</p>
  </a>
  <a href="04-pyspark/" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">4</span>
    <h3>PySpark Transform</h3>
    <p>Write the Spark job that cleans and loads the data.</p>
  </a>
  <a href="05-dbt-models/" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">5</span>
    <h3>dbt Models</h3>
    <p>Create staging and mart models with tests.</p>
  </a>
  <a href="06-run/" class="feature-card" style="text-decoration:none">
    <span class="feature-icon">6</span>
    <h3>Run End-to-End</h3>
    <p>Trigger the DAG, verify results, open Grafana.</p>
  </a>
</div>

[Begin: Init & Install →](01-init.md){ .md-button .md-button--primary }
