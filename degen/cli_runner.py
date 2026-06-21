import os
import subprocess
from rich.console import Console
from rich.rule import Rule

console = Console()


def run_project_command(name: str, config) -> None:
    """Execute a named command from degen.yaml with real-time output."""
    if not config.has_command(name):
        available = "  ".join(f"degen {c}" for c in config.available_commands())
        console.print(
            f"\n[bold red]✗ Command '[cyan]{name}[/cyan]' is not available "
            f"in a [bold]{config.pattern}[/bold] project.[/bold red]\n"
        )
        console.print(f"[dim]Available commands: {available}[/dim]\n")
        raise SystemExit(1)

    cmd_cfg = config.commands[name]

    # Run dependencies first
    for dep in cmd_cfg.get("deps", []):
        run_project_command(dep, config)

    steps = cmd_cfg.get("steps", [])
    if not steps:
        return

    # Build env: OS + .env file
    env = {**os.environ}
    env_file = config.root / ".env"
    if env_file.exists():
        from dotenv import dotenv_values
        env.update({k: v for k, v in dotenv_values(env_file).items() if v is not None})

    console.print(Rule(f"[bold green]degen {name}[/bold green]"))

    for step in steps:
        console.print(f"[dim]$ {step}[/dim]")
        result = subprocess.run(step, shell=True, cwd=config.root, env=env)
        if result.returncode != 0:
            console.print(f"\n[bold red]✗ Failed (exit {result.returncode})[/bold red]")
            raise SystemExit(result.returncode)

    console.print(f"[bold green]✓ Done[/bold green]\n")
