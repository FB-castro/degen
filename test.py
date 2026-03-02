from degen.patterns.batch import BatchPattern
from degen.composer.composer import Composer

pattern = BatchPattern()

Composer.compose(
    project_name="test_project",
    pattern=pattern,
    selected_tool_names=["Python", "DuckDB", "dbt"]
)