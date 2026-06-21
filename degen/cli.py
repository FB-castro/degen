import subprocess
import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich.rule import Rule
from rich import print

from degen.version import __version__

from degen.patterns.batch import BatchPattern
from degen.patterns.analytics import AnalyticsPattern
from degen.patterns.streaming import StreamingPattern
from degen.tools.registry import TOOL_REGISTRY
from degen.composer.composer import Composer
from degen.core.phases import Phase
from degen.core.project_config import load_config
from degen.cli_runner import run_project_command

app = typer.Typer(
    help="DEGEN — Data Engineering Project Generator",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


def print_header():
    console.print(
        Panel.fit(
            f"[bold green]DEGEN[/bold green] v{__version__}\n"
            "[dim]Data Engineering Project Generator[/dim]",
            border_style="green",
        )
    )


def get_patterns():
    return {
        "Batch ETL":  BatchPattern(),
        "Analytics":  AnalyticsPattern(),
        "Streaming":  StreamingPattern(),
    }


def get_tools_by_phase(phase: Phase):
    return [
        tool_class()
        for tool_class in TOOL_REGISTRY.values()
        if tool_class().phase == phase
    ]


def _build_tree(branch, path, depth=0):
    for child in sorted(path.iterdir()):
        if child.name.startswith(".") or child.name == "__pycache__":
            continue
        if child.is_dir():
            subtree = branch.add(f"[bold blue]{child.name}/[/bold blue]")
            if depth < 2:
                _build_tree(subtree, child, depth + 1)
        else:
            branch.add(child.name)


def _next_step_cmds(pattern_name, selected_tools, project_name):
    tool_names = {t.name for t in selected_tools}
    cmds = [f"cd {project_name}", "degen install"]

    if pattern_name == "Streaming":
        cmds += ["degen docker-up", "degen produce", "degen stream"]
    elif pattern_name == "Batch ETL":
        cmds.append("degen run")
        if "dbt" in tool_names:
            cmds += ["degen seed", "degen test"]
    elif pattern_name == "Analytics":
        if "Airflow" in tool_names:
            cmds += ["degen docker-up", "degen orchestrate"]
        elif "Prefect" in tool_names:
            cmds += ["degen prefect-server", "degen run"]
        if {"Metabase", "Grafana"} & tool_names:
            cmds.append("degen serve")

    return cmds


def _project_cmd(name: str):
    config = load_config()
    run_project_command(name, config)


# ─── Init ──────────────────────────────────────────────────────────────────

@app.command()
def init():
    """Initialize a new Data Engineering project."""

    print_header()

    project_name = questionary.text("Project name:").ask()
    if not project_name:
        console.print("[red]Project name is required.[/red]")
        raise typer.Exit()

    patterns = get_patterns()
    pattern_name = questionary.select(
        "Select architecture pattern:",
        choices=list(patterns.keys()),
    ).ask()
    pattern = patterns[pattern_name]

    selected_tools = []
    for phase in pattern.required_phases:
        tools_for_phase = get_tools_by_phase(phase)
        if not tools_for_phase:
            console.print(f"[red]No tools available for phase: {phase}[/red]")
            raise typer.Exit()

        tool_names = [t.name for t in tools_for_phase]
        selected_name = questionary.select(
            f"  [{phase.value.upper()}] Select tool:",
            choices=tool_names,
        ).ask()
        selected_tools.append(next(t for t in tools_for_phase if t.name == selected_name))

    # Summary
    console.print()
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column(style="bold")
    table.add_row("Project", project_name)
    table.add_row("Pattern", pattern_name)
    table.add_row("Tools", " + ".join(t.name for t in selected_tools))
    console.print(table)
    console.print()

    pattern.validate_tools(selected_tools)

    with console.status("[bold green]Generating project...", spinner="dots"):
        root = Composer.compose(
            project_name=project_name,
            pattern=pattern,
            selected_tools=selected_tools,
        )

    # File tree
    tree = Tree(f"[bold green]{project_name}/[/bold green]")
    _build_tree(tree, root)
    console.print(tree)
    console.print()

    # Next steps
    cmds = _next_step_cmds(pattern_name, selected_tools, project_name)
    steps_text = "\n".join(f"  [cyan]{cmd}[/cyan]" for cmd in cmds)
    console.print(
        Panel(
            steps_text,
            title="[bold green]Next steps[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
    )


# ─── Status ────────────────────────────────────────────────────────────────

@app.command()
def status():
    """Show project info, available commands and Docker service health."""
    config = load_config()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column(style="bold")
    table.add_row("Project", config.project)
    table.add_row("Pattern", config.pattern)
    table.add_row("Tools", ", ".join(config.tools))
    table.add_row("Location", str(config.root))
    console.print(Panel(table, title="[bold green]DEGEN Project[/bold green]", border_style="green"))

    console.print("\n[bold]Available commands:[/bold]")
    for cmd in config.available_commands():
        console.print(f"  [cyan]degen {cmd}[/cyan]")

    if config.ui:
        console.print("\n[bold]Web UIs:[/bold]")
        for name, url in config.ui.items():
            console.print(f"  [bold]{name}[/bold]  →  [cyan]{url}[/cyan]")

    result = subprocess.run(
        "docker compose ps --format 'table {{.Name}}\\t{{.Status}}'",
        shell=True, cwd=config.root, capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        console.print(Rule("[dim]Docker services[/dim]"))
        console.print(result.stdout)


@app.command()
def ui():
    """List all web UIs available in this project."""
    config = load_config()
    if not config.ui:
        console.print("[dim]No web UIs defined for this project.[/dim]")
        return

    table = Table(title=f"[bold green]Web UIs — {config.project}[/bold green]", box=None, padding=(0, 3))
    table.add_column("Tool", style="bold")
    table.add_column("URL", style="cyan")
    for name, url in config.ui.items():
        table.add_row(name, url)
    console.print(table)


# ─── Project commands ──────────────────────────────────────────────────────

@app.command()
def install():
    """Install project dependencies."""
    _project_cmd("install")


@app.command()
def run():
    """Run the data pipeline."""
    _project_cmd("run")


@app.command()
def stream():
    """Start the streaming job (PySpark + Kafka)."""
    _project_cmd("stream")


@app.command()
def produce():
    """Produce sample events to Kafka."""
    _project_cmd("produce")


@app.command()
def seed():
    """Run dbt seed."""
    _project_cmd("seed")


@app.command()
def test():
    """Run dbt tests."""
    _project_cmd("test")


@app.command()
def serve():
    """Start the serving layer (Metabase / Grafana)."""
    _project_cmd("serve")


@app.command()
def orchestrate():
    """Show Airflow DAG info and UI URL."""
    _project_cmd("orchestrate")


@app.command(name="docker-up")
def docker_up():
    """Start all Docker services (docker compose up -d)."""
    _project_cmd("docker-up")


@app.command(name="docker-down")
def docker_down():
    """Stop and remove Docker services."""
    _project_cmd("docker-down")


@app.command(name="create-topic")
def create_topic():
    """Create Kafka topic defined in .env."""
    _project_cmd("create-topic")


@app.command(name="prefect-server")
def prefect_server():
    """Start Prefect UI server."""
    _project_cmd("prefect-server")


@app.command()
def notebook():
    """Launch Jupyter Lab for interactive data exploration."""
    _project_cmd("notebook")


@app.command()
def docs():
    """Generate and serve dbt documentation."""
    _project_cmd("docs")


@app.command()
def exec(command: str = typer.Argument(..., help="Command name from degen.yaml")):
    """Run any named command defined in degen.yaml."""
    _project_cmd(command)


# ─── Version ───────────────────────────────────────────────────────────────

@app.command()
def version():
    """Show installed version."""
    print(f"degen {__version__}")


if __name__ == "__main__":
    app()
