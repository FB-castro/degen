import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich import print

from degen.version import __version__

from degen.patterns.batch import BatchPattern
from degen.patterns.analytics import AnalyticsPattern
from degen.tools.registry import TOOL_REGISTRY
from degen.composer.composer import Composer
from degen.core.phases import Phase

app = typer.Typer(help="🚀 Degen — Architecture Composer")
console = Console()


# -------------------------
# Helpers
# -------------------------

def print_header():
    console.print(
        Panel.fit(
            f"[bold green]DEGEN[/bold green]\nVersion: {__version__}",
            border_style="green"
        )
    )


def get_patterns():
    return {
        "Batch ETL": BatchPattern(),
        "Analytics": AnalyticsPattern(),
    }


def get_tools_by_phase(phase: Phase):

    tools = []

    for tool_class in TOOL_REGISTRY.values():
        tool_instance = tool_class()
        if tool_instance.phase == phase:
            tools.append(tool_instance)

    return tools


# -------------------------
# CLI Commands
# -------------------------

@app.command()
def init():
    """
    Initialize a new Data Engineering project.
    """

    print_header()

    # 1️⃣ Project name
    project_name = questionary.text(
        "Project name:"
    ).ask()

    if not project_name:
        console.print("[red]Project name is required.[/red]")
        raise typer.Exit()

    # 2️⃣ Select pattern
    patterns = get_patterns()

    pattern_name = questionary.select(
        "Select architecture pattern:",
        choices=list(patterns.keys())
    ).ask()

    pattern = patterns[pattern_name]

    selected_tools = []

    # 3️⃣ For each required phase, choose tool
    for phase in pattern.required_phases:

        tools_for_phase = get_tools_by_phase(phase)

        if not tools_for_phase:
            console.print(f"[red]No tools available for phase: {phase}[/red]")
            raise typer.Exit()

        tool_names = [tool.name for tool in tools_for_phase]

        selected_name = questionary.select(
            f"Select tool for phase '{phase.value}':",
            choices=tool_names
        ).ask()

        selected_tool = next(
            tool for tool in tools_for_phase
            if tool.name == selected_name
        )

        selected_tools.append(selected_tool)

    # 4️⃣ Validate pattern
    pattern.validate_tools(selected_tools)

    # 5️⃣ Compose project
    Composer.compose(
        project_name=project_name,
        pattern=pattern,
        selected_tools=selected_tools
    )

    console.print(
        f"""
        [bold green]Project '{project_name}' created successfully![/bold green]

        Next steps:

        cd {project_name}
        make install
        make run
        """
        )


@app.command()
def version():
    """Show installed version"""
    print(f"Degen version: {__version__}")


if __name__ == "__main__":
    app()