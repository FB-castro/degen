from degen.patterns.base import Pattern
from degen.core.phases import Phase


class StreamingPattern(Pattern):

    name = "Streaming"

    required_phases = [
        Phase.STREAM,
        Phase.TRANSFORM,
        Phase.STORE,
    ]

    def validate_tools(self, tools):
        selected_phases = {tool.phase for tool in tools}
        missing = set(self.required_phases) - selected_phases
        if missing:
            raise ValueError(f"Missing required phases: {missing}")
