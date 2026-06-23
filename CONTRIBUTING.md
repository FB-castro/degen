# Contributing to DEGEN

Thanks for your interest in contributing. DEGEN is open source and welcomes contributions of all kinds — bug fixes, new tool integrations, documentation improvements, and ideas.

## Getting started

```bash
git clone https://github.com/FB-castro/degen.git
cd degen
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Verify your setup:

```bash
degen --version
degen --help
```

## How to contribute

### Report a bug

Open an issue using the **Bug Report** template. Include your OS, DEGEN version, the pattern you selected, and the full error output.

### Request a feature

Open an issue using the **Feature Request** template. Describe the problem it solves — not just what you want, but why.

### Submit a pull request

1. Fork the repo and create a branch: `git checkout -b feat/my-change`
2. Make your changes
3. Test locally: `degen init`, `degen install`, `degen run`
4. Open a PR using the pull request template

### Add a new tool

Each tool lives in `degen/tools/<phase>/<tool>.py` and extends the `Tool` base class from `degen/tools/base.py`.

The tool must implement:

```python
def get_docker_services(self) -> dict       # Docker Compose services
def get_requirements(self) -> list[str]     # pip dependencies
def get_makefile_targets(self) -> dict      # CLI commands (steps)
def get_ui_urls(self) -> dict[str, str]     # web UI name → URL
```

Then register it in `degen/tools/registry.py`.

## Project structure

```
degen/
  cli.py              # Typer CLI commands
  cli_runner.py       # executes degen.yaml commands with Rich output
  core/
    project_config.py # reads degen.yaml, finds project root
    phases.py         # phase definitions (Extract, Transform, etc.)
  patterns/           # Batch ETL, Analytics, Streaming
  tools/              # one file per tool
  composer/           # project generation logic
```

## Questions?

Open a [GitHub Discussion](https://github.com/FB-castro/degen/discussions) — not an issue.
