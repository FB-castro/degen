import typer
import questionary
import subprocess
import sys
from importlib.metadata import version, PackageNotFoundError

from rich.console import Console

from degen.registry.pattern_registry import PatternRegistry
from degen.core.generator import generate_project
from degen.core.logger import configure_logger, logger

app = typer.Typer(
    help="""
Generate production-ready data engineering architectures.

Create real-world project scaffolds including Docker,
.env configuration, virtual environments and working examples.
""",
    no_args_is_help=True,
)

console = Console()


def get_version():
    try:
        return version("degen")
    except PackageNotFoundError:
        return "0.0.0-dev"


@app.callback()
def main(
    version_flag: bool = typer.Option(
        None,
        "--version",
        help="Show DEGEN version.",
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable debug logs.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error logs.",
    ),
):
    if version_flag:
        console.print(f"degen v{get_version()}")
        raise typer.Exit()

    configure_logger(verbose=verbose, quiet=quiet)


# --------------------------------------------------
# INIT
# --------------------------------------------------

@app.command(help="Create a new project.")
def init(
    name: str = typer.Option(None, "--name", help="Project name"),
    pattern: str = typer.Option(None, "--pattern", help="Architecture pattern"),
    stack: str = typer.Option(None, "--stack", help="Technology stack"),
    debug: bool = typer.Option(False, "--debug", help="Show full error trace"),
):
    """
    Create a new project.

    Examples:
      degen init
      degen init --name myproj --pattern Analytics --stack "dbt + DuckDB"
    """

    logger.info("Resolving available patterns...")
    patterns = PatternRegistry.list_patterns()

    if not patterns:
        logger.error("No patterns registered.")
        raise typer.Exit(code=1)

    if not name:
        name = questionary.text("Project name:").ask()

    if not name:
        logger.error("Project name is required.")
        raise typer.Exit(code=1)

    if not pattern:
        pattern = questionary.select(
            "Select a pattern:",
            choices=patterns,
        ).ask()

    if pattern not in patterns:
        logger.error(f"Invalid pattern: {pattern}")
        raise typer.Exit(code=1)

    pattern_obj = PatternRegistry.get(pattern)
    available_stacks = pattern_obj.supported_stacks

    if not stack:
        stack = questionary.select(
            "Select a stack:",
            choices=available_stacks,
        ).ask()

    if stack not in available_stacks:
        logger.error(f"Invalid stack for {pattern}: {stack}")
        raise typer.Exit(code=1)

    try:
        logger.info("Creating project structure...")
        logger.debug(f"Pattern selected: {pattern}")
        logger.debug(f"Stack selected: {stack}")

        generate_project(name, pattern, stack)

        logger.info(f"Project '{name}' created successfully.")
        logger.info("Next steps:")
        logger.info(f"  cd {name}")
        logger.info("  make install")
        logger.info("  make run")

    except Exception as e:
        if debug:
            raise
        logger.error(f"Error generating project: {e}")
        raise typer.Exit(code=1)


# --------------------------------------------------
# LIST
# --------------------------------------------------

@app.command(name="list", help="Show available patterns and stacks.")
def list_cmd():
    patterns = PatternRegistry.list_patterns()

    if not patterns:
        logger.error("No patterns registered.")
        raise typer.Exit(code=1)

    for pattern_name in patterns:
        pattern_obj = PatternRegistry.get(pattern_name)
        logger.info(f"\n{pattern_name}")
        for stack in pattern_obj.supported_stacks:
            logger.info(f"  - {stack}")


# --------------------------------------------------
# DOCTOR
# --------------------------------------------------

@app.command(help="Check required system dependencies.")
def doctor():
    checks = []

    python_ok = sys.version_info >= (3, 12)
    checks.append(("Python >= 3.12", python_ok))

    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        docker_ok = True
    except Exception:
        docker_ok = False
    checks.append(("Docker installed", docker_ok))

    try:
        subprocess.run(["make", "--version"], check=True, capture_output=True)
        make_ok = True
    except Exception:
        make_ok = False
    checks.append(("Make available", make_ok))

    for label, status in checks:
        symbol = "✓" if status else "✗"
        if status:
            logger.info(f"{symbol} {label}")
        else:
            logger.error(f"{symbol} {label}")

    if all(status for _, status in checks):
        logger.info("\nEnvironment ready.")
    else:
        logger.error("\nMissing dependencies detected.")


# --------------------------------------------------
# INFO
# --------------------------------------------------

@app.command(help="Show information about DEGEN installation.")
def info():
    logger.info(f"DEGEN version: {get_version()}")
    logger.info(f"Python version: {sys.version.split()[0]}")
    logger.info(f"Executable: {sys.executable}")
    logger.info(f"Registered patterns: {len(PatternRegistry.list_patterns())}")