# 5. dbt Models

In this step you'll create two dbt models that transform the raw Postgres staging data into clean analytical tables.

---

## dbt project structure

After `degen install`, your dbt project lives at `sales_pipeline/`. The structure:

```
sales_pipeline/           ← dbt project root
├── dbt_project.yml
├── models/
│   └── example/          ← generated examples (you can delete these)
└── tests/
```

You'll create two new models:

```
models/
  staging/
    stg_sales.sql         ← clean up the raw Postgres table
    stg_sales.yml         ← schema + tests
  marts/
    sales_summary.sql     ← aggregate by product and region
    sales_summary.yml     ← schema + tests
```

---

## Create the staging model

Create `sales_pipeline/models/staging/stg_sales.sql`:

```sql title="sales_pipeline/models/staging/stg_sales.sql" linenums="1"
-- Staging model: read from the Postgres table loaded by PySpark,
-- cast types explicitly, and filter out any bad rows.
with source as (
    select * from {{ source('staging', 'staging_sales') }}
),

cleaned as (
    select
        date::date                      as sale_date,
        trim(lower(product))            as product,
        trim(lower(region))             as region,
        quantity::int                   as quantity,
        price::numeric(10, 2)           as unit_price,
        (quantity * price)::numeric(10, 2) as revenue
    from source
    where
        date is not null
        and quantity > 0
        and price > 0
)

select * from cleaned
```

Create `sales_pipeline/models/staging/stg_sales.yml`:

```yaml title="sales_pipeline/models/staging/stg_sales.yml" linenums="1"
version: 2

sources:
  - name: staging
    schema: public
    tables:
      - name: staging_sales
        description: "Raw sales table loaded by PySpark."

models:
  - name: stg_sales
    description: "Cleaned and typed sales records."
    columns:
      - name: sale_date
        description: "Date of the sale."
        tests:
          - not_null

      - name: product
        description: "Product name (lowercased)."
        tests:
          - not_null

      - name: region
        description: "Sales region (lowercased)."
        tests:
          - not_null
          - accepted_values:
              values: ["north", "south", "east", "west"]

      - name: quantity
        tests:
          - not_null

      - name: unit_price
        tests:
          - not_null

      - name: revenue
        tests:
          - not_null
```

---

## Create the mart model

Create `sales_pipeline/models/marts/sales_summary.sql`:

```sql title="sales_pipeline/models/marts/sales_summary.sql" linenums="1"
-- Mart model: aggregate daily sales by product and region.
-- This is the table Grafana will query for dashboards.
with base as (
    select * from {{ ref('stg_sales') }}
)

select
    sale_date,
    product,
    region,
    sum(quantity)              as total_units,
    sum(revenue)               as total_revenue,
    avg(unit_price)::numeric(10,2) as avg_price,
    count(*)                   as num_transactions
from base
group by
    sale_date,
    product,
    region
order by
    sale_date desc,
    total_revenue desc
```

Create `sales_pipeline/models/marts/sales_summary.yml`:

```yaml title="sales_pipeline/models/marts/sales_summary.yml" linenums="1"
version: 2

models:
  - name: sales_summary
    description: "Daily aggregated sales by product and region."
    columns:
      - name: sale_date
        tests:
          - not_null

      - name: product
        tests:
          - not_null

      - name: total_revenue
        description: "Sum of revenue for this product/region/day."
        tests:
          - not_null
```

---

## Update dbt_project.yml

Tell dbt to materialize staging as views and marts as tables:

```yaml title="sales_pipeline/dbt_project.yml" linenums="1"
name: sales_pipeline
version: '1.0.0'
config-version: 2

profile: sales_pipeline

model-paths: ["models"]
seed-paths:  ["seeds"]
test-paths:  ["tests"]

models:
  sales_pipeline:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

---

## Run dbt manually

Test both models before Airflow runs them:

```bash
degen seed    # optional: load any seed CSVs
```

```bash
cd sales_pipeline && ../.venv/bin/dbt run --profiles-dir ..
```

```
18:42:01  1 of 2 START sql view model public.stg_sales .................. [RUN]
18:42:01  1 of 2 OK created sql view model public.stg_sales ............. [CREATE VIEW in 0.41s]
18:42:01  2 of 2 START sql table model public.sales_summary .............. [RUN]
18:42:02  2 of 2 OK created sql table model public.sales_summary ......... [SELECT 200 in 0.58s]
18:42:02  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2
```

Run the tests:

```bash
cd sales_pipeline && ../.venv/bin/dbt test --profiles-dir ..
```

```
18:42:05  1 of 8 PASS not_null_stg_sales_sale_date
18:42:05  2 of 8 PASS not_null_stg_sales_product
18:42:05  3 of 8 PASS accepted_values_stg_sales_region
18:42:05  4 of 8 PASS not_null_stg_sales_revenue
18:42:05  5 of 8 PASS not_null_sales_summary_sale_date
18:42:05  6 of 8 PASS not_null_sales_summary_product
18:42:05  7 of 8 PASS not_null_sales_summary_total_revenue
18:42:05  Done. PASS=7 WARN=0 ERROR=0
```

---

## Browse the lineage graph

```bash
degen docs
```

Open **http://localhost:8081** and click on `sales_summary` in the lineage graph. You'll see the full chain:

```
staging_sales (Postgres)  →  stg_sales (view)  →  sales_summary (table)
```

Click any model to see its compiled SQL, column descriptions, and test results.

---

## View data in pgAdmin

Open **http://localhost:5050** → DEGEN Postgres → degen → Schemas → public → Tables.

You'll see:
- `staging_sales` — 200 raw rows from PySpark
- `sales_summary` — ~20 rows (200 rows aggregated by product × region × date)

[Next: Run End-to-End →](06-run.md){ .md-button .md-button--primary }
