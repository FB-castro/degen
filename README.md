# DEGEN

Data Engineering Generator CLI

## ✨ Features

- Batch ETL (DuckDB)
- ELT (Airflow + Postgres)
- Medallion (Spark + MinIO)
- Analytics (dbt + DuckDB)

## 🚀 Install

```bash
pipx install degen
```
## 🧑‍💻 Usage

```bash
degen init
```

## Non-interactive Usage

```bash
degen init --name myproj --pattern Analytics --stack "dbt + DuckDB"
```

## Doctor

```bash
degen doctor
```

| Pattern   | Stack   |
| --------- | ------- |
| Batch     | DuckDB  |
| ELT       | Airflow |
| Medallion | Spark   |
| Analytics | dbt     |


📌 Roadmap

 Spark + Iceberg

 dbt + Postgres

 Streaming (Flink)

 Plugin system

 SaaS mode