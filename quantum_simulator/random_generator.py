class RandomGenerator:
    """
    Random generator class
    """

    m: int
    "m value"

    a: int
    "a value"

    c: int
    "c value"

    seed: int
    "generator seed"

    X: int
    "current generator value"

    def __init__(self, m=65537, a=75, c=74, seed=27):
        """
        RandomGenerator initializer
        """
        self.m = m
        self.a = a
        self.c = c
        self.seed = seed
        self.X = self.generate_initial_num(seed, n0=99)

    def rand_int(self):
        """Returns random integer value. Updates self"""
        self.X = (self.a * self.X + self.c) % self.m
        return self.X

    def rand(self, L=None):
        """Returns random number. Updates self"""
        self.X = self.rand_int()
        return self.X / self.m if L is None else (self.X / self.m - 0.5) * 2 * L

    def generate_initial_num(self, seed, n0):
        """Skips `n0` random numbers"""
        self.X = seed
        for _ in range(n0):
            self.X = self.rand_int()
        return self.X
