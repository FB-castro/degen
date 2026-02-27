import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import subprocess
import sys


from degen.registry.pattern_registry import PatternRegistry
from degen.core.generator import generate_project

app = typer.Typer()
console = Console()


def print_header():
    header = Text("DEGEN", style="bold green")
    subtitle = Text("Data Engineering Generator CLI", style="dim")

    panel = Panel(
        Align.center(header + "\n" + subtitle),
        border_style="green",
        padding=(1, 4),
    )

    console.print(panel)


@app.command()
def init(
    name: str = typer.Option(None, "--name", help="Nome do projeto"),
    pattern: str = typer.Option(None, "--pattern", help="Pattern a usar"),
    stack: str = typer.Option(None, "--stack", help="Stack a usar"),
    debug: bool = typer.Option(False, "--debug", help="Modo debug"),
):
    """
    Inicializa um novo projeto de engenharia de dados.
    """

    print_header()

    patterns = PatternRegistry.list_patterns()

    if not patterns:
        console.print("[bold red]Nenhum pattern registrado.[/bold red]")
        raise typer.Exit(code=1)

    # 🔹 Nome
    if not name:
        name = questionary.text("Nome do projeto:").ask()

    if not name:
        console.print("[bold red]Nome do projeto é obrigatório.[/bold red]")
        raise typer.Exit(code=1)

    # 🔹 Pattern
    if not pattern:
        pattern = questionary.select(
            "Escolha o Pattern:",
            choices=patterns,
        ).ask()

    if pattern not in patterns:
        console.print(f"[bold red]Pattern inválido:[/bold red] {pattern}")
        raise typer.Exit(code=1)

    pattern_obj = PatternRegistry.get(pattern)

    # 🔹 Stack
    available_stacks = pattern_obj.supported_stacks

    if not stack:
        stack = questionary.select(
            "Escolha a Stack:",
            choices=available_stacks,
        ).ask()

    if stack not in available_stacks:
        console.print(f"[bold red]Stack inválida para {pattern}:[/bold red] {stack}")
        raise typer.Exit(code=1)

    # 🔹 Geração
    try:
        with console.status(
            "[bold green]Gerando projeto...[/bold green]",
            spinner="dots",
        ):
            generate_project(name, pattern, stack)

    except Exception as e:
        if debug:
            raise
        console.print(f"[bold red]Erro ao gerar projeto:[/bold red] {e}")
        raise typer.Exit(code=1)

    summary = f"""
Projeto: {name}
Pattern: {pattern}
Stack: {stack}

Próximos passos:
  cd {name}
  make install
  make run
"""

    console.print(
        Panel(summary.strip(), title="✔ Projeto Criado", border_style="green")
    )


@app.command()
def doctor():
    """
    Verifica dependências do ambiente.
    """

    print_header()

    checks = []

    # Python
    python_ok = sys.version_info >= (3, 12)
    checks.append(("Python >= 3.12", python_ok))

    # Docker
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        docker_ok = True
    except Exception:
        docker_ok = False
    checks.append(("Docker instalado", docker_ok))

    # Make
    try:
        subprocess.run(["make", "--version"], check=True, capture_output=True)
        make_ok = True
    except Exception:
        make_ok = False
    checks.append(("Make disponível", make_ok))

    for label, status in checks:
        color = "green" if status else "red"
        console.print(f"[{color}]✔ {label}[/{color}]" if status else f"[red]✘ {label}[/red]")

    if all(status for _, status in checks):
        console.print("\n[bold green]Ambiente pronto para usar o degen.[/bold green]")
    else:
        console.print("\n[bold red]Existem dependências faltando.[/bold red]")


