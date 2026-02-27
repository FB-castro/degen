from typing import Dict, Type
from degen.stacks.base import Stack


class StackRegistry:
    _stacks: Dict[str, Type[Stack]] = {}

    @classmethod
    def register(cls, stack: Type[Stack]):
        cls._stacks[stack.name] = stack

    @classmethod
    def get(cls, name: str) -> Stack:
        return cls._stacks[name]()

    @classmethod
    def list_stacks(cls):
        return list(cls._stacks.keys())