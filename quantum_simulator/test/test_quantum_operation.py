"""Quantum operations tests module"""

from unittest import TestCase

import numpy as np
import pytest

from quantum_simulator.quantum_operation import OneQubitOperation, TwoQubitsOperation


@pytest.mark.quant_oper
class TestQuantumOperation(TestCase):
    """QuantumOperation tests class"""

    def test_one_qubit_init(self):
        """Tests OneQubitOperation init"""
        X_mtrx = np.array([[0, 1], [1, 0]])

        with self.assertRaises(TypeError):
            X = OneQubitOperation([[0, 1], [1, 0]], target_qubits=[1])

        with self.assertRaises(ValueError):
            X = OneQubitOperation(X_mtrx.flatten(), target_qubits=[1])

        with self.assertRaises(TypeError):
            X = OneQubitOperation(X_mtrx, target_qubits=1)

        X = OneQubitOperation(X_mtrx, target_qubits=[1])
        self.assertTrue((X.matrix == X_mtrx).all())
        self.assertEqual(X.target_qubits, [1])

    def test_two_qubits_init(self):
        """Tests TwoQubitsOperation init"""
        CZ_mtrx = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])

        with self.assertRaises(TypeError):
            CZ = TwoQubitsOperation([[0, 1], [1, 0]], target_qubits=[1])

        with self.assertRaises(ValueError):
            CZ = TwoQubitsOperation(CZ_mtrx.flatten(), target_qubits=[1])

        with self.assertRaises(TypeError):
            CZ = TwoQubitsOperation(CZ_mtrx, target_qubits=1)

        with self.assertRaises(ValueError):
            CZ = TwoQubitsOperation(CZ_mtrx, target_qubits=[1])

        CZ = TwoQubitsOperation(CZ_mtrx, target_qubits=[1, 2])
        self.assertTrue((CZ.matrix == CZ_mtrx).all())
        self.assertEqual(CZ.target_qubits, [1, 2])

    def test_identity(self):
        """Tests I matrices"""
        I1 = OneQubitOperation.I()
        self.assertEqual(I1.matrix.shape, (2, 2))
        self.assertTrue((I1.matrix == np.eye(2)).all())

        I2 = TwoQubitsOperation.I()
        self.assertEqual(I2.matrix.shape, (4, 4))
        self.assertTrue((I2.matrix == np.eye(4)).all())

    def test_custom_operations(self):
        """Tests all Pauli matrices basic properties"""
        I = OneQubitOperation.I()
        X = OneQubitOperation.X()
        Y = OneQubitOperation.Y()
        Z = OneQubitOperation.Z()

        for sigma in [X, Y, Z]:
            # sigma^dagger == sigma
            self.assertTrue((np.conj(sigma.matrix).T == sigma.matrix).all())

            # Tr(sigma) == 0
            self.assertEqual(np.trace(sigma.matrix), 0)

            # sigma^2 = I
            square = sigma.matrix @ sigma.matrix
            self.assertTrue((square == I.matrix).all())

        XY = X.matrix @ Y.matrix
        self.assertTrue((XY == 1j * Z.matrix).all())

        ZX = Z.matrix @ X.matrix
        self.assertTrue((ZX == 1j * Y.matrix).all())

        YZ = Y.matrix @ Z.matrix
        self.assertTrue((YZ == 1j * X.matrix).all())

        # sigma_i @ sigma_j == -1 * sigma_j @ sigma_i
        for i, sigma_i in enumerate([X, Y, Z]):
            for j, sigma_j in enumerate([X, Y, Z]):
                if i == j:
                    continue
                self.assertTrue((sigma_i.matrix @ sigma_j.matrix == -1 * sigma_j.matrix @ sigma_i.matrix).all())
