from abc import ABC, abstractmethod

class PseudoRNG(ABC):
    def __init__(self, seed):
        self.seed = seed
        self._state = self._initial_state(seed)

    @abstractmethod
    def _initial_state(self, seed):
        ...

    @abstractmethod
    def next(self):
        ...

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def generate(self, n):
        return [self.next() for _ in range(n)]
