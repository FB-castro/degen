class Validator:

    @staticmethod
    def validate(pattern, selected_tools):
        tool_names = {tool.name for tool in selected_tools}

        if "dbt" in tool_names:
            sql_stores = {"DuckDB", "Postgres", "ClickHouse"}
            if not tool_names & sql_stores:
                raise ValueError(
                    f"dbt requires a SQL store. Choose one of: {sorted(sql_stores)}"
                )

        if "Metabase" in tool_names or "Grafana" in tool_names:
            sql_stores = {"DuckDB", "Postgres", "ClickHouse"}
            if not tool_names & sql_stores:
                raise ValueError(
                    "Visualization tools (Metabase, Grafana) require a SQL store."
                )

        if "Kafka" in tool_names and "PySpark" not in tool_names:
            raise ValueError(
                "Kafka streaming requires PySpark as the transform tool."
            )

        if "PySpark" in tool_names and "Kafka" in tool_names:
            stores = {"Postgres", "ClickHouse"}
            if not tool_names & stores:
                raise ValueError(
                    "Streaming pipeline (Kafka + PySpark) requires Postgres or ClickHouse as the store."
                )
