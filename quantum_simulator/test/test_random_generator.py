"""Random generator tests module"""

from unittest import TestCase

import numpy as np
import pytest

from quantum_simulator.random_generator import RandomGenerator


@pytest.mark.random
class TestRandomGenerator(TestCase):
    """RandomGenerator tests class"""

    def test_random_generator_init(self):
        """Tests RandomGenerator init"""
        rand_gen = RandomGenerator()
        self.assertEqual(rand_gen.state, 14715)
        self.assertEqual(rand_gen.m, 65537)
        self.assertEqual(rand_gen.a, 75)
        self.assertEqual(rand_gen.c, 74)
        self.assertEqual(rand_gen.seed, 27)

        # check that generator properties are read-only
        with self.assertRaises(AttributeError):
            rand_gen.state = 0
        with self.assertRaises(AttributeError):
            rand_gen.m = 0
        with self.assertRaises(AttributeError):
            rand_gen.a = 0
        with self.assertRaises(AttributeError):
            rand_gen.c = 0
        with self.assertRaises(AttributeError):
            rand_gen.seed = 0

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

    def test_get_rand_unitary(self):
        """Tests RandomGenerator rand_unitary()"""
        rand_gen = RandomGenerator()
        U1 = rand_gen.rand_unitary("1q")
        target_U1 = np.array([[-0.15993173 - 0.31217771j, 0.87691877 + 0.32860369j], [-0.22080244 + 0.9100622j, 0.16840845 + 0.30768763j]])
        self.assertTrue(np.isclose(U1, target_U1).all())

        U2 = rand_gen.rand_unitary("2q")
        target_U2 = np.array(
            [
                [-0.3719458 - 0.01701984j, 0.1913409 - 0.176701j, 0.72057625 + 0.39256476j, -0.33574361 - 0.08643538j],
                [0.60583561 + 0.35087279j, 0.45208891 + 0.36159583j, 0.09476359 - 0.00109205j, -0.38687635 - 0.12673169j],
                [-0.05039977 + 0.22385688j, 0.57039366 - 0.04917816j, 0.16956984 + 0.01920575j, 0.76592686 + 0.06175591j],
                [0.49953428 - 0.26273866j, -0.46268193 + 0.2349202j, 0.51836348 + 0.14091826j, 0.35152864 - 0.00638688j],
            ]
        )
        self.assertTrue(np.isclose(U2, target_U2).all())
