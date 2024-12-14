"""Random generator tests module"""

from unittest import TestCase

import pytest

from quantum_simulator.random_generator import RandomGenerator


@pytest.mark.quant_oper
class TestQuantumOperation(TestCase):
    """RandomGenerator tests class"""

    def test_random_generator_init(self):
        """Tests RandomGenerator init"""
        rand_gen = RandomGenerator()
        self.assertEqual(rand_gen.X, 14715)
        self.assertEqual(rand_gen.m, 65537)
        self.assertEqual(rand_gen.a, 75)
        self.assertEqual(rand_gen.c, 74)
        self.assertEqual(rand_gen.seed, 27)

    def test_random_generator_rand(self):
        """Tests RandomGenerator rand()"""
        rand_gen = RandomGenerator()
        rand_float = rand_gen.rand()
        self.assertAlmostEqual(rand_float, 0.8408532584646841)
        rand_float = rand_gen.rand()
        self.assertAlmostEqual(rand_float, 0.06512351801272563)
        rand_float = rand_gen.rand()
        self.assertAlmostEqual(rand_float, 0.885392984115843)

    def test_random_generator_rand_int(self):
        """Tests RandomGenerator rand_int()"""
        rand_gen = RandomGenerator()
        rand_int = rand_gen.rand_int()
        self.assertEqual(rand_int, 55107)
        rand_int = rand_gen.rand_int()
        self.assertEqual(rand_int, 4268)
        rand_int = rand_gen.rand_int()
        self.assertEqual(rand_int, 58026)
