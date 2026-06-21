from pathlib import Path
from degen.core.phases import Phase

from degen.composer.validator import Validator
from degen.composer.docker_builder import DockerBuilder
from degen.composer.project_builder import ProjectBuilder


class Composer:

    @staticmethod
    def compose(project_name, pattern, selected_tools):

        Validator.validate(pattern, selected_tools)

        store_tool = next(
            (t for t in selected_tools if t.phase == Phase.STORE), None
        )
        stream_tool = next(
            (t for t in selected_tools if t.phase == Phase.STREAM), None
        )

        for tool in selected_tools:
            if tool.name == "dbt" and store_tool:
                tool.configure_store(store_tool)
            if tool.name == "PySpark" and stream_tool:
                tool.configure_stream(stream_tool)

        docker_content = DockerBuilder.build(selected_tools)

        root = Path.cwd() / project_name

        ProjectBuilder.build(
            root=root,
            project_name=project_name,
            pattern_name=pattern.name,
            selected_tools=selected_tools,
            docker_compose_content=docker_content,
        )

        return root
