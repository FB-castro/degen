class Validator:

    @staticmethod
    def validate(pattern, selected_tools):
        # Exemplo regra: dbt precisa storage SQL
        tool_names = [tool.name for tool in selected_tools]

        if "dbt" in tool_names:
            if not any(store in tool_names for store in ["DuckDB", "Postgres"]):
                raise ValueError("dbt requires DuckDB or Postgres as storage")

        if "Metabase" in tool_names:
            if not any(store in tool_names for store in ["DuckDB", "Postgres"]):
                raise ValueError("Metabase requires SQL storage")