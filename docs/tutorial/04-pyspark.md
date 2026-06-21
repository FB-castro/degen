# 4. PySpark Transformation

In this step you'll write the Spark job that reads the raw CSV, cleans the data, and loads it into Postgres.

---

## Create the script

Create the file `src/pyspark_transform.py`:

```python title="src/pyspark_transform.py" linenums="1"
"""
PySpark job: read raw sales CSV → clean → load to Postgres staging table.
"""
from pathlib import Path
import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, IntegerType, DateType


PROJECT_ROOT = Path(__file__).parent.parent
RAW_FILE     = PROJECT_ROOT / "data" / "raw" / "sales.csv"

PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_DB   = os.getenv("POSTGRES_DB",   "degen")
PG_USER = os.getenv("POSTGRES_USER", "degen")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "degen")

JDBC_URL = f"jdbc:postgresql://{PG_HOST}:{PG_PORT}/{PG_DB}"


def get_spark() -> SparkSession:
    # The PostgreSQL JDBC driver must be on the classpath.
    # requirements.txt installs pyspark; the JDBC jar is downloaded here automatically.
    return (
        SparkSession.builder
        .appName("degen-sales-transform")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.7.3",
        )
        .getOrCreate()
    )


def read_raw(spark: SparkSession):
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(RAW_FILE))
    )


def clean(df):
    return (
        df
        # Cast columns to correct types
        .withColumn("date",     F.col("date").cast(DateType()))
        .withColumn("quantity", F.col("quantity").cast(IntegerType()))
        .withColumn("price",    F.col("price").cast(DoubleType()))
        # Derived: total revenue per row
        .withColumn("revenue",  F.round(F.col("quantity") * F.col("price"), 2))
        # Remove rows with nulls in key columns
        .dropna(subset=["date", "product", "region", "quantity", "price"])
        # Normalize region to lowercase
        .withColumn("region", F.lower(F.col("region")))
    )


def load_to_postgres(df) -> None:
    (
        df.write
        .format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", "staging_sales")
        .option("user", PG_USER)
        .option("password", PG_PASS)
        .option("driver", "org.postgresql.Driver")
        .mode("overwrite")           # truncate + reload on each run
        .save()
    )


def main():
    print(f"Reading: {RAW_FILE}")
    spark = get_spark()

    raw = read_raw(spark)
    print(f"Raw rows: {raw.count()}")
    raw.printSchema()

    cleaned = clean(raw)
    print(f"Clean rows: {cleaned.count()}")
    cleaned.show(5, truncate=False)

    print(f"Loading to Postgres → staging_sales")
    load_to_postgres(cleaned)
    print("Done.")

    spark.stop()


if __name__ == "__main__":
    main()
```

---

## Run it manually

Before connecting Airflow, test the script directly:

```bash
degen run
```

Or run the script directly:

```bash
.venv/bin/python src/pyspark_transform.py
```

Expected output:

```
Reading: /path/to/sales_pipeline/data/raw/sales.csv
Raw rows: 200
root
 |-- date: string (nullable = true)
 |-- product: string (nullable = true)
 |-- region: string (nullable = true)
 |-- quantity: integer (nullable = true)
 |-- price: double (nullable = true)

Clean rows: 200
+----------+---------+------+--------+------+-------+
|date      |product  |region|quantity|price |revenue|
+----------+---------+------+--------+------+-------+
|2024-01-01|Widget A |north |12      |49.99 |599.88 |
|2024-01-01|Gadget X |south |3       |129.99|389.97 |
...
Loading to Postgres → staging_sales
Done.
```

---

## Inspect in pgAdmin

Open **http://localhost:5050** → Servers → DEGEN Postgres → degen → Schemas → public → Tables.

You'll see `staging_sales` with 200 rows. Right-click → **View/Edit Data → All Rows** to browse the records.

---

## Open the Spark UI

While the Spark job runs (it takes ~30 seconds), open:

**http://localhost:4040**

The Spark UI shows:

- **Jobs** — the JDBC write job with task count and duration
- **SQL** — the DataFrame query plan
- **Executors** — memory and CPU usage

The UI closes when `spark.stop()` is called, so check it while the job is running.

---

## How it works

```
sales.csv   ─read→   Spark DataFrame   ─clean→   Spark DataFrame   ─write→   Postgres
               (200 rows)                (200 rows)                  (staging_sales)
```

The key operations:

| Operation | What it does |
|---|---|
| `.cast(DateType())` | Converts string `"2024-01-01"` to a proper date |
| `.withColumn("revenue", ...)` | Adds a derived column `quantity × price` |
| `.dropna(...)` | Removes incomplete rows |
| `.mode("overwrite")` | Truncates the table before each load |

[Next: Write the dbt Models →](05-dbt-models.md){ .md-button .md-button--primary }
