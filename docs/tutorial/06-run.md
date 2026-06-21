# 6. Run End-to-End

In this step you'll trigger the full pipeline from Airflow and verify the results in every tool.

---

## Trigger the DAG

Open **http://localhost:8080** and find `sales_pipeline` in the list.

Enable the DAG with the toggle on the left, then click the **▶ Run** button (top right of the DAG page) to trigger a manual run.

Or trigger from the terminal:

```bash
.venv/bin/airflow dags trigger sales_pipeline
```

---

## Watch the execution

Click on the DAG name → **Graph** view. Watch the tasks change color as they run:

| Color | Meaning |
|---|---|
| Grey | Queued |
| Yellow | Running |
| Green | Success |
| Red | Failed |

The full run takes about 60–90 seconds:

```
extract            ~2s     ← generates 200 CSV rows
pyspark_transform  ~45s    ← Spark start-up + JDBC write to Postgres
dbt_run            ~5s     ← creates stg_sales view + sales_summary table
dbt_test           ~5s     ← runs 7 tests
```

---

## Inspect the task logs

Click any task → **Logs** tab to see its full output. For `pyspark_transform`:

```
[2024-01-01 18:42:01] INFO - Reading: /path/to/sales_pipeline/data/raw/sales.csv
[2024-01-01 18:42:01] INFO - Raw rows: 200
[2024-01-01 18:42:43] INFO - Clean rows: 200
[2024-01-01 18:42:44] INFO - Loading to Postgres → staging_sales
[2024-01-01 18:42:45] INFO - Done.
[2024-01-01 18:42:45] INFO - Task exited with return code 0
```

For `dbt_test`:

```
18:42:05  Done. PASS=7 WARN=0 ERROR=0
```

---

## Verify data in pgAdmin

Open **http://localhost:5050**.

Navigate to: Servers → DEGEN Postgres → degen → Schemas → public → Tables.

Right-click **sales_summary** → **View/Edit Data → All Rows**.

You'll see the aggregated results:

| sale_date | product | region | total_units | total_revenue | avg_price | num_transactions |
|---|---|---|---|---|---|---|
| 2024-01-01 | widget a | north | 312 | 8,412.50 | 74.99 | 9 |
| 2024-01-01 | gadget x | south | 187 | 15,302.13 | 129.99 | 7 |
| ... | ... | ... | ... | ... | ... | ... |

---

## Build a Grafana dashboard

Open **http://localhost:3001** → **Connections → Data Sources → Add**.

Select **PostgreSQL** and fill in:

| Field | Value |
|---|---|
| Host | `postgres:5432` |
| Database | `degen` |
| User | `degen` |
| Password | `degen` |
| TLS/SSL | Disable |

Click **Save & Test** — it should say "Database Connection OK".

### Create a dashboard

Go to **Dashboards → New → New Dashboard → Add visualization**.

Select the Postgres data source. In the query editor (SQL mode), enter:

```sql
SELECT
  sale_date AS "time",
  product,
  total_revenue
FROM sales_summary
ORDER BY sale_date
```

Set visualization to **Time series**. You'll see a revenue line per product over time.

Add a second panel:

```sql
SELECT
  region,
  SUM(total_revenue) AS revenue
FROM sales_summary
GROUP BY region
ORDER BY revenue DESC
```

Set visualization to **Bar chart** — revenue by region.

Click **Save dashboard** and name it `Sales Overview`.

---

## Schedule recurring runs

The DAG is already set to `schedule="@daily"`. To change it, edit `dags/pipeline_dag.py`:

```python
# Run every day at 6am
schedule="0 6 * * *",

# Run every hour
schedule="@hourly",

# Run every Monday at 9am
schedule="0 9 * * 1",
```

Save the file — Airflow picks up the change within 30 seconds with no restart.

---

## What you built

You now have a complete Analytics pipeline:

```
[Airflow scheduler]
        │
        ▼ every day
   extract task
        │ generates 200 sales rows
        ▼
pyspark_transform task
        │ cleans + loads to Postgres (staging_sales)
        ▼
    dbt_run task
        │ creates stg_sales view + sales_summary table
        ▼
   dbt_test task
        │ validates 7 data quality rules
        ▼
   [Grafana dashboard]
        │ reads from sales_summary
        ▼
  revenue by product & region
```

And you can inspect every layer:

| Tool | What you see | URL |
|---|---|---|
| Airflow | Pipeline runs, task logs, schedules | :8080 |
| pgAdmin | Raw Postgres tables, SQL queries | :5050 |
| dbt Docs | Lineage graph, model SQL, test results | :8081 |
| Grafana | Revenue dashboards | :3001 |
| Spark UI | Job execution plan (during PySpark run) | :4040 |

---

## Next steps

- Add more dbt models (customer metrics, product rankings)
- Add Airflow sensors to trigger the DAG when a file lands
- Connect a real data source in `dags/pipeline_dag.py` → `run_extract()`
- Add Slack alerts on DAG failure via Airflow connections

[Back to Tutorial Overview](index.md){ .md-button }
[Browse all Patterns](../patterns/analytics.md){ .md-button .md-button--primary }
