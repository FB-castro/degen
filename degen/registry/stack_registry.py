from typing import Dict, Type, List
from degen.stacks.base import Stack


class StackRegistry:
    _stacks: Dict[str, Type[Stack]] = {}

    @classmethod
    def register(cls, stack: Type[Stack]) -> None:
        cls._stacks[stack.name] = stack

    @classmethod
    def get(cls, name: str) -> Stack:
        if name not in cls._stacks:
            available = ", ".join(cls._stacks.keys()) or "none"
            raise ValueError(
                f"Stack '{name}' não encontrada. Disponíveis: {available}"
            )
        return cls._stacks[name]()

    @classmethod
    def list_stacks(cls) -> List[str]:
        return list(cls._stacks.keys())

    @classmethod
    def exists(cls, name: str) -> bool:
        return name in cls._stacks