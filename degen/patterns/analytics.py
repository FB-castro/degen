from degen.patterns.base import Pattern
from degen.core.phases import Phase


class AnalyticsPattern(Pattern):

    name = "Analytics"

    required_phases = [
        Phase.ORCHESTRATE,
        Phase.TRANSFORM,
        Phase.STORE,
        Phase.SERVE,
    ]

    def validate_tools(self, tools):

        selected_phases = {tool.phase for tool in tools}
        missing = set(self.required_phases) - selected_phases

        if missing:
            raise ValueError(f"Missing required phases: {missing}")