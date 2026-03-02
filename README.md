# 🚀 DEGEN — Data Engineering Project Generator

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.5.3-brightgreen)

Opinionated CLI for generating production-ready data engineering scaffolds.

DEGEN creates structured, working data engineering projects with:

- Virtual environment setup
- dbt integration
- Dynamic store configuration (DuckDB or Postgres)
- Automatic `.env` generation
- Docker support
- Makefile orchestration

---

## ✨ Current Features (v0.5.3)

### 🏗 Architecture
- Batch ETL pattern
- One tool per phase (extract, transform, store)
- Pattern validation before project generation

### 🔌 Supported Tools

#### Extract
- Python

#### Transform
- dbt (1.7.x)

#### Store
- DuckDB
- Postgres

---

## ⚙️ What DEGEN Generates

Each generated project includes:

- Structured project scaffold
- `.env` file with tool-specific variables
- `requirements.txt` with pinned dependencies
- Dynamic `Makefile` with install/run/test targets
- `docker-compose.yml`
- dbt project initialized automatically
- dbt `profiles.yml` generated dynamically based on selected store

---

## 🚀 Installation

### Recommended

```bash
pipx install degen
```

### Development

```bash
git clone https://github.com/FB-castro/degen.git
cd degen
pipx install -e .
```

---

## ⚡ Usage

### Initialize a new project

```bash
degen init
```

The CLI will prompt you to:

1. Choose project name  
2. Select architecture pattern  
3. Select one tool per phase (extract, transform, store)

---

## 📦 Example Generated Project

Example (Python + dbt + DuckDB):

```
my_project/
├── data/
│   ├── raw/
│   └── warehouse.duckdb
├── src/
│   └── extract.py
├── my_project/          # dbt project
├── docker-compose.yml
├── requirements.txt
├── .env
├── Makefile
```

Example (Python + dbt + Postgres):

```
my_project/
├── data/
│   └── raw/
├── src/
│   └── extract.py
├── my_project/          # dbt project
├── docker-compose.yml
├── requirements.txt
├── .env
├── Makefile
```

---

## ▶ Running a Generated Project

```bash
cd my_project
make install
make run
make test
```

Start infrastructure (if store uses Docker):

```bash
make docker-up
```

Stop infrastructure:

```bash
make docker-down
```

---

## 🔐 Environment Configuration

DEGEN automatically generates a `.env` file including:

- PROJECT_NAME
- DBT_THREADS
- DUCKDB_PATH (if DuckDB selected)
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

The Makefile and Docker configuration consume these variables automatically.

---

## 🧠 Design Philosophy

DEGEN is:

- Opinionated
- Minimal
- Extensible
- Stack-aware
- Environment-driven

It favors clarity and explicit architecture over template sprawl.

---

## 🛣 Next Major Version (v0.6.0)

The next release will introduce:

- Pattern-defined base project structure
- More structured directory layout
- Improved Docker networking
- Stronger separation between pattern and tool responsibilities

---

## 📄 License

MIT