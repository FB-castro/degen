from abc import ABC, abstractmethod
from degen.core.phases import Phase


class Pattern(ABC):

    name: str
    required_phases: list[Phase]

    @abstractmethod
    def validate_tools(self, tools):
        pass