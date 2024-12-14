"""Random generator module"""

import numpy as np
import scipy as sc


class RandomGenerator:
    """
    Random generator class
    """

    _m: int
    "m value"

    _a: int
    "a value"

    _c: int
    "c value"

    _seed: int
    "generator seed"

    _X: int
    "current generator value"

    def __init__(self, m: int = 65537, a: int = 75, c: int = 74, seed: int = 27):
        """
        RandomGenerator initializer
        """
        self._m = m
        self._a = a
        self._c = c
        self._seed = seed
        self._state = self.generate_initial_num(seed, n0=99)

    def rand_int(self):
        """Returns random integer value. Updates self"""
        self._state = (self.a * self._state + self.c) % self.m
        return self._state

    def rand(self, L: int = None):
        """Returns random number. Updates self"""
        self._state = self.rand_int()
        return self._state / self.m if L is None else (self._state / self.m - 0.5) * 2 * L

    def generate_initial_num(self, seed: int, n0: int):
        """Skips `n0` random numbers"""
        self._state = seed
        for _ in range(n0):
            self._state = self.rand_int()
        return self._state

    @property
    def m(self):
        """RandomGenerator._m readonly getter"""
        return self._m

    @property
    def a(self):
        """RandomGenerator._a readonly getter"""
        return self._a

    @property
    def c(self):
        """RandomGenerator._c readonly getter"""
        return self._c

    @property
    def seed(self):
        """RandomGenerator._seed readonly getter"""
        return self._seed

    @property
    def state(self):
        """RandomGenerator._state readonly getter"""
        return self._state

    def rand_unitary(self, mode: str) -> np.ndarray:
        """Builds and returns random unitary matrix using random generator"""
        assert mode in ["1q", "2q"], f"'{mode}' mode is not supported, should be '1q' or '2q'"
        if mode == "1q":
            c = [self.rand(L=100) for _ in range(4)]
            U = 1j * np.array([[c[0], c[1] + 1j * c[2]], [c[1] - 1j * c[2], c[3]]])
        else:
            c = [self.rand(L=100) for _ in range(16)]
            U = 1j * np.array(
                [
                    [c[0], c[1] + 1j * c[2], c[3] + 1j * c[4], c[5] + 1j * c[6]],
                    [c[1] - 1j * c[2], c[7], c[8] + 1j * c[9], c[10] + 1j * c[11]],
                    [c[3] - 1j * c[4], c[8] - 1j * c[9], c[12], c[13] + 1j * c[14]],
                    [c[5] - 1j * c[6], c[10] - 1j * c[11], c[13] - 1j * c[14], c[15]],
                ]
            )
        return sc.linalg.expm(U)
