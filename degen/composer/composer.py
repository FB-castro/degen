from pathlib import Path
from degen.core.phases import Phase

from degen.composer.validator import Validator
from degen.composer.docker_builder import DockerBuilder
from degen.composer.project_builder import ProjectBuilder


class Composer:

    @staticmethod
    def compose(project_name, pattern, selected_tools):

        # selected_tools já são INSTÂNCIAS
        Validator.validate(pattern, selected_tools)

        store_tool = next(
            (tool for tool in selected_tools if tool.phase == Phase.STORE),
            None
        )

        for tool in selected_tools:
            if tool.name.lower() == "dbt" and store_tool:
                tool.configure_store(store_tool)


        docker_content = DockerBuilder.build(selected_tools)

        root = Path.cwd() / project_name

        ProjectBuilder.build(
            root=root,
            selected_tools=selected_tools,
            docker_compose_content=docker_content,
        )

        return root