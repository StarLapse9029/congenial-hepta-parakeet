from prng_class import PseudoRNG

class LCG(PseudoRNG):
    def __init__(self, seed, modulus=2**31, multiplier=1103515245, increment=12345):
        """Linear Congruential Generator Implementation\nUsing glibc(GCC)/ANSIC parameters as default"""
        self.modulus = modulus
        self.multiplier = multiplier
        self.increment = increment
        super().__init__(seed)

    def _initial_state(self, seed):
        return seed

    def next(self):
        self._state = (self.multiplier * self._state + self.increment) % self.modulus
        return self._state
