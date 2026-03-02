from pathlib import Path
import textwrap

class ProjectBuilder:

    @staticmethod
    def build(root: Path, selected_tools, docker_compose_content):

        root.mkdir(parents=True, exist_ok=True)


        # Docker
        (root / "docker-compose.yml").write_text(docker_compose_content)


        # Requirements
        dependencies = []
        for tool in selected_tools:
            dependencies.extend(tool.get_python_dependencies())

        (root / "requirements.txt").write_text(
            "\n".join(sorted(set(dependencies)))
        )


        # Project structure
        for tool in selected_tools:
            structure = tool.get_project_structure()

            for folder, files in structure.items():
                folder_path = root / folder
                folder_path.mkdir(parents=True, exist_ok=True)

                for filename, content in files.items():
                    (folder_path / filename).write_text(content)
        

        # .env generation 
        env_vars = {
            "PROJECT_NAME": root.name
        }

        for tool in selected_tools:
            tool_env = getattr(tool, "get_env_variables", lambda: {})()
            env_vars.update(tool_env)

        env_content = "\n".join(
            f"{key}={value}" for key, value in env_vars.items()
        )

        (root / ".env").write_text(env_content + "\n")



        # Makefile composition (dynamic targets)
        tool_targets = {}

        for tool in selected_tools:
            targets = tool.get_makefile_targets()

            for target_name, commands in targets.items():
                tool_targets.setdefault(target_name, []).extend(commands)

        makefile = textwrap.dedent(f"""
        .PHONY: venv install run seed test run-all clean docker-up docker-down

        include .env
        export $(shell sed 's/=.*//' .env)

        VENV = .venv
        PYTHON = $(VENV)/bin/python
        PIP = $(VENV)/bin/pip

        venv:
        \tpython -m venv $(VENV)

        install: venv
        \t$(PIP) install -r requirements.txt
        """)

        # Inject dynamic targets
        for target_name, commands in tool_targets.items():

            if target_name == "install":
                for cmd in commands:
                    makefile += f"\t{cmd}\n"
                continue

            makefile += f"\n{target_name}:\n"

            if commands:
                for cmd in commands:
                    makefile += f"\t{cmd}\n"
            else:
                makefile += "\t@echo \"Nothing to execute\"\n"

        # Run-all orchestration
        makefile += textwrap.dedent("""
        run-all: run seed test
        """)

        makefile += textwrap.dedent(f"""
        clean:
        \trm -rf $(VENV)
        \trm -rf data/*.duckdb
        \trm -rf */target */logs

        docker-up:
        \tdocker compose up -d

        docker-down:
        \tdocker compose down
        """)

        (root / "Makefile").write_text(makefile.strip() + "\n")

        return root