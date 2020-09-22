from __future__ import annotations


from copy import deepcopy
from typing import Tuple, Union
from collections import deque
from . import evaluator


NoneType = type(None)


class Context:

    def fork(self) -> Context:
        return deepcopy(self)
    
    def forkwith(self, name: str, value: evaluator.Value) -> Context:
        new = self.fork()
        new.add((name, value))
        return new

    def get(self, name: str) -> Union[evaluator.Value, NoneType]:
        for (key, value) in self.items:
            if name == key:
                return value
        else:
            return None

    def add(self, item: Tuple[str, evaluator.Value]):
        self.items.appendleft(item)

    def __init__(self) -> None:
        self.items = deque()
