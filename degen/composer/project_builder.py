from pathlib import Path
import textwrap
import yaml

from degen.core.phases import Phase


class ProjectBuilder:

    @staticmethod
    def build(
        root: Path,
        project_name: str,
        pattern_name: str,
        selected_tools,
        docker_compose_content: str,
    ):

        root.mkdir(parents=True, exist_ok=True)

        # Docker Compose
        (root / "docker-compose.yml").write_text(docker_compose_content)

        # requirements.txt
        dependencies = []
        for tool in selected_tools:
            dependencies.extend(tool.get_python_dependencies())
        (root / "requirements.txt").write_text(
            "\n".join(sorted(set(dependencies))) + "\n"
        )

        # Project structure (dirs + template files)
        for tool in selected_tools:
            for folder, files in tool.get_project_structure().items():
                folder_path = root / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                for filename, content in files.items():
                    (folder_path / filename).write_text(content)

        # .env
        env_vars = {"PROJECT_NAME": project_name}
        for tool in selected_tools:
            env_vars.update(tool.get_env_variables())
        env_content = "\n".join(f"{k}={v}" for k, v in env_vars.items()) + "\n"
        (root / ".env").write_text(env_content)

        # profiles.yml (written directly — consumed by dbt with --profiles-dir ..)
        dbt_tool = next((t for t in selected_tools if t.name == "dbt"), None)
        if dbt_tool:
            profiles_yaml = dbt_tool.build_profiles_yaml(project_name)
            if profiles_yaml:
                (root / "profiles.yml").write_text(profiles_yaml)

        # Makefile (kept for CI/power users)
        ProjectBuilder._write_makefile(root, selected_tools)

        # degen.yaml — primary project manifest
        ProjectBuilder._write_degen_yaml(root, project_name, pattern_name, selected_tools)

        return root

    @staticmethod
    def _write_makefile(root: Path, selected_tools):
        tool_targets: dict[str, list[str]] = {}

        for tool in selected_tools:
            for target_name, commands in tool.get_makefile_targets().items():
                tool_targets.setdefault(target_name, []).extend(commands)

        all_targets = ["venv", "install", "run", "seed", "test", "stream",
                       "produce", "serve", "orchestrate", "prefect-server",
                       "run-all", "clean", "docker-up", "docker-down"]
        phony = " ".join(all_targets)

        makefile = textwrap.dedent(f"""\
        .PHONY: {phony}

        include .env
        export $(shell sed 's/=.*//' .env)

        VENV   = .venv
        PYTHON = $(VENV)/bin/python
        PIP    = $(VENV)/bin/pip

        venv:
        \tpython -m venv $(VENV)

        install: venv
        \t$(PIP) install --upgrade pip
        \t$(PIP) install -r requirements.txt
        """)

        # inject install extras from tools
        if "install" in tool_targets:
            for cmd in tool_targets.pop("install"):
                makefile += f"\t{cmd}\n"

        # all other dynamic targets
        for target_name, commands in tool_targets.items():
            makefile += f"\n{target_name}:\n"
            for cmd in commands:
                makefile += f"\t{cmd}\n"

        # run-all: only include targets that were actually contributed by tools
        _RUN_ALL_CANDIDATES = ["run", "seed", "test", "produce", "stream", "serve"]
        run_all_deps = " ".join(t for t in _RUN_ALL_CANDIDATES if t in tool_targets)
        if run_all_deps:
            makefile += f"\nrun-all: {run_all_deps}\n"
        else:
            makefile += "\nrun-all:\n\t@echo 'No run-all targets defined for this pattern'\n"

        makefile += textwrap.dedent("""
        clean:
        \trm -rf $(VENV)
        \trm -rf data/*.duckdb data/processed
        \trm -rf */target */logs

        docker-up:
        \tdocker compose up -d

        docker-down:
        \tdocker compose down -v
        """)

        (root / "Makefile").write_text(makefile)

    @staticmethod
    def _write_degen_yaml(root: Path, project_name: str, pattern_name: str, selected_tools):
        commands: dict = {
            "install": {
                "steps": [
                    "python -m venv .venv",
                    ".venv/bin/pip install --upgrade pip",
                    ".venv/bin/pip install -r requirements.txt",
                ]
            },
            "docker-up":   {"steps": ["docker compose up -d"]},
            "docker-down": {"steps": ["docker compose down -v"]},
        }

        for tool in selected_tools:
            for cmd_name, cmd_cfg in tool.get_cli_commands(project_name).items():
                if cmd_name not in commands:
                    commands[cmd_name] = {"steps": []}
                commands[cmd_name].setdefault("steps", []).extend(cmd_cfg.get("steps", []))
                for dep in cmd_cfg.get("deps", []):
                    deps_list = commands[cmd_name].setdefault("deps", [])
                    if dep not in deps_list:
                        deps_list.append(dep)

        ui_urls: dict = {}
        for tool in selected_tools:
            ui_urls.update(tool.get_ui_urls())

        config = {
            "project": project_name,
            "pattern": pattern_name,
            "tools": [t.name for t in selected_tools],
            "ui": ui_urls,
            "commands": commands,
        }

        (root / "degen.yaml").write_text(yaml.dump(config, sort_keys=False))
