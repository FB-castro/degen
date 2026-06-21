# Batch ETL

Extract data from sources, transform it with dbt, and persist it in a SQL database.

**Best for:** scheduled pipelines, data warehousing, analytics engineering.

---

## Tools

| Phase | Options |
|---|---|
| Extract | Python |
| Transform | dbt |
| Store | DuckDB · Postgres |

---

## Create the project

```bash
degen init
```

Select **Batch ETL**, then choose your tools. This guide uses **Python + dbt + DuckDB**.

```bash
cd my_batch_project
```

---

## Install

```bash
degen install
```

This will:

1. Create `.venv`
2. Install pandas, dbt-core, dbt-duckdb, duckdb
3. Run `dbt init` to scaffold the dbt project structure

Expected output:
```
degen install
──────────────
$ python -m venv .venv
$ .venv/bin/pip install -r requirements.txt
...Successfully installed dbt-core dbt-duckdb duckdb pandas
$ .venv/bin/dbt init my_batch_project --skip-profile-setup
Your new dbt project "my_batch_project" was created!
✓ Done
```

---

## Run the pipeline

```bash
degen run
```

Runs extract → dbt in sequence:

```
degen run
──────────
$ .venv/bin/python src/extract.py
INFO  Extracted 3 rows
   id   name  value
0   1  Alice    100
1   2    Bob    200
2   3  Carol    300

$ cd my_batch_project && ../.venv/bin/dbt run --profiles-dir ..
18:52:29  1 of 2 OK created sql table model main.my_first_dbt_model
18:52:29  2 of 2 OK created sql view model main.my_second_dbt_model
✓ Done
```

---

## Seed and test

```bash
degen seed   # load seed CSV files into DuckDB
degen test   # run dbt data quality tests
```

Expected test output:
```
18:52:35  1 of 4 PASS not_null_my_first_dbt_model_id
18:52:35  2 of 4 PASS unique_my_first_dbt_model_id
18:52:35  Done. PASS=4 WARN=0 ERROR=0
```

---

## Explore with Jupyter

```bash
degen notebook
```

Opens Jupyter Lab at **http://localhost:8888**.

Query the DuckDB warehouse directly from a notebook:

```python
import duckdb

con = duckdb.connect("data/warehouse.duckdb", read_only=True)
con.sql("SHOW TABLES").show()
con.sql("SELECT * FROM my_first_dbt_model").show()
con.close()
```

!!! tip
    Always use `read_only=True` or call `con.close()` in the notebook before running `degen run` or `degen docs` — DuckDB allows only one write connection at a time.

---

## Browse dbt documentation

```bash
degen docs
```

Generates the dbt documentation site and serves it at **http://localhost:8081**.

You'll see:

- Data lineage graph
- Model descriptions and column docs
- Test results
- Source definitions

---

## Project structure

```
my_batch_project/
├── degen.yaml              # project manifest
├── .env                    # environment variables
├── requirements.txt        # pinned dependencies
├── profiles.yml            # dbt connection config
├── docker-compose.yml      # no services for DuckDB (file-based)
├── data/
│   ├── raw/
│   │   └── sample.csv      # source data
│   └── warehouse.duckdb    # generated after degen run
├── notebooks/              # place your Jupyter notebooks here
├── src/
│   └── extract.py          # extraction script
└── my_batch_project/       # dbt project
    ├── dbt_project.yml
    ├── models/
    │   └── example/
    │       ├── my_first_dbt_model.sql
    │       └── my_second_dbt_model.sql
    └── seeds/
```

---

## Customizing the extractor

Edit `src/extract.py` to connect to your real data source:

```python
import pandas as pd

def extract() -> pd.DataFrame:
    # Replace with your real source:
    # df = pd.read_sql("SELECT * FROM orders", engine)
    # df = pd.read_csv("s3://bucket/file.csv")
    df = pd.read_csv("data/raw/sample.csv")
    df.to_parquet("data/raw/output.parquet", index=False)
    return df
```

---

## Using Postgres instead of DuckDB

Select **Postgres** as the store during `degen init`. DEGEN will:

- Add `postgres:16` to `docker-compose.yml`
- Add **pgAdmin 4** at `http://localhost:5050`
- Generate a Postgres-compatible `profiles.yml`

```bash
degen docker-up   # start Postgres + pgAdmin
degen run         # extract + dbt run against Postgres
```

pgAdmin credentials: `admin@degen.io` / `degen`
