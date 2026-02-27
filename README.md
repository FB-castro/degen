# 🚀 DEGEN — Data Engineering Generator

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.3.0-brightgreen)
![CI](https://github.com/FB-castro/degen/actions/workflows/ci.yml/badge.svg)

Generate production-ready data engineering architectures in seconds.

DEGEN is a modern CLI that scaffolds real-world data engineering systems — complete with Docker, environment configuration, virtual environments, and working examples.


---

## ✨ Features

- 🏗 Batch ETL (DuckDB)
- 🔄 ELT (Airflow + Postgres)
- 🏞 Medallion (Spark + MinIO)
- 📊 Analytics Engineering (dbt + DuckDB)
- 🐳 Docker-ready stacks
- 🧪 Local execution with `.venv`
- 🩺 Environment validation (`doctor`)
- ℹ Installation info (`info`)
- 🔎 Structured logging
- ⚡ Interactive + non-interactive mode

---

## 🚀 Installation

### Recommended

```bash
pipx install degen
```

### Development

```bash
git clone https://github.com/youruser/degen.git
cd degen
pipx install -e .
```

---

## ⚡ Commands

### Initialize a project

Interactive:

```bash
degen init
```

Non-interactive:

```bash
degen init --name myproj --pattern Analytics --stack "dbt + DuckDB"
```

---

### List patterns and stacks

```bash
degen list
```

---

### Validate environment

```bash
degen doctor
```

---

### Show installation info

```bash
degen info
```

---

## 🔧 Global Flags

| Flag | Description |
|------|------------|
| `--version` | Show DEGEN version |
| `--verbose` / `-v` | Enable debug logs |
| `--quiet` / `-q` | Suppress non-error logs |

Example:

```bash
degen init --name myproj -v
```

---

## 🧱 Example Generated Structure

```text
my_project/
├── src/
├── models/
├── data/
├── lake/
├── requirements.txt
├── .env
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ▶ Running a Generated Project

```bash
cd my_project
make install
make run
```

Or:

```bash
make docker-up
```

---

## 🛣 Roadmap

- [ ] Spark + Iceberg
- [ ] dbt + Postgres
- [ ] Streaming (Flink)
- [ ] Plugin system
- [ ] Template marketplace
- [ ] SaaS version

---

## 📄 License

[MIT](LICENSE)