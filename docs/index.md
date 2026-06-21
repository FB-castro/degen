---
hide:
  - navigation
  - toc
---

<div class="hero">
  <div class="hero-badge">Open Source · v0.7.0</div>
  <h1>The Data Engineering<br>Framework</h1>
  <p>One command to scaffold any data pipeline. Every tool wired, every service running, every UI ready — in minutes, not hours.</p>
  <div class="hero-install">$ pipx install degen</div>
  <div class="hero-links">
    <a href="tutorial/index.md" class="primary">Start Tutorial →</a>
    <a href="getting-started.md" class="secondary">Getting Started</a>
    <a href="https://github.com/FB-castro/degen" class="secondary">GitHub</a>
  </div>
</div>

<div class="feature-grid">
  <div class="feature-card">
    <span class="feature-icon">⚡</span>
    <h3>Interactive Scaffold</h3>
    <p>Answer three questions. DEGEN generates a complete, working project tailored to your stack.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">🐋</span>
    <h3>Services Out of the Box</h3>
    <p>Kafka, Postgres, Airflow, Grafana — all in Docker, pre-wired, one <code>degen docker-up</code>.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">🖥️</span>
    <h3>Web UI for Everything</h3>
    <p>Every tool ships with its own interface. No manual config — UIs are registered and opened automatically.</p>
  </div>
  <div class="feature-card">
    <span class="feature-icon">🚀</span>
    <h3>Unified CLI</h3>
    <p><code>degen run</code>, <code>degen stream</code>, <code>degen docs</code> — one consistent interface regardless of the stack.</p>
  </div>
</div>

---

## Architecture Patterns

<div class="pattern-grid">
  <a href="patterns/batch-etl.md" class="pattern-card">
    <div class="pattern-card-label">Pattern 01</div>
    <h3>Batch ETL</h3>
    <p>Extract, transform with dbt, and persist in DuckDB or Postgres. Explore results in Jupyter.</p>
    <div class="tools">Python · dbt · DuckDB · Postgres</div>
    <div class="arrow">Read guide →</div>
  </a>
  <a href="patterns/analytics.md" class="pattern-card">
    <div class="pattern-card-label">Pattern 02</div>
    <h3>Analytics</h3>
    <p>Orchestrate scheduled pipelines with Prefect or Airflow. Visualize with Grafana or Metabase.</p>
    <div class="tools">Airflow · dbt · Postgres · Grafana</div>
    <div class="arrow">Read guide →</div>
  </a>
  <a href="patterns/streaming.md" class="pattern-card">
    <div class="pattern-card-label">Pattern 03</div>
    <h3>Streaming</h3>
    <p>Real-time event processing with Kafka and PySpark Structured Streaming.</p>
    <div class="tools">Kafka · PySpark · ClickHouse</div>
    <div class="arrow">Read guide →</div>
  </a>
</div>

---

## Every Tool Has a Web UI

<div class="ui-grid">
  <div class="ui-card">
    <div class="tool-name">Kafka</div>
    <div class="ui-name">Kafka UI</div>
    <div class="port">:8082</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">Postgres</div>
    <div class="ui-name">pgAdmin 4</div>
    <div class="port">:5050</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">Airflow</div>
    <div class="ui-name">Airflow UI</div>
    <div class="port">:8080</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">Prefect</div>
    <div class="ui-name">Prefect UI</div>
    <div class="port">:4200</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">Grafana</div>
    <div class="ui-name">Grafana</div>
    <div class="port">:3001</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">Metabase</div>
    <div class="ui-name">Metabase</div>
    <div class="port">:3000</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">dbt</div>
    <div class="ui-name">dbt Docs</div>
    <div class="port">:8081</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">DuckDB</div>
    <div class="ui-name">Jupyter Lab</div>
    <div class="port">:8888</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">PySpark</div>
    <div class="ui-name">Spark UI</div>
    <div class="port">:4040</div>
  </div>
  <div class="ui-card">
    <div class="tool-name">ClickHouse</div>
    <div class="ui-name">Play UI</div>
    <div class="port">:8123/play</div>
  </div>
</div>

---

## The Hands-On Tutorial

The best way to understand DEGEN is to build something real.

The [Tutorial](tutorial/index.md) walks you through creating a full Analytics pipeline from zero — Airflow + PySpark + dbt + Postgres — writing every file yourself, running every command, and seeing results in the UI.

[Start the Tutorial →](tutorial/index.md){ .md-button .md-button--primary }
