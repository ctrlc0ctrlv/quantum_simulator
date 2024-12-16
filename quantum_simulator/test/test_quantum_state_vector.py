"""Quantum state vector tests module"""

from unittest import TestCase

import numpy as np
import pytest
from qiskit.quantum_info import Statevector as QiskitStateVector

from quantum_simulator.quantum_state_vector import QuantumStateVector


@pytest.mark.quant_state_vector
class TestQuantumStateVector(TestCase):
    """QuantumStateVector tests class"""

    def test_quantum_state_vector_init_from_int(self):
        """Tests QuantumStateVector init from int"""

        quant_state_vec = QuantumStateVector(1)
        self.assertTrue(quant_state_vec is not None)
        self.assertEqual(quant_state_vec.length, 2)
        self.assertEqual(quant_state_vec[0], 1)
        self.assertEqual(quant_state_vec[1], 0)
        self.assertEqual(quant_state_vec.vector, [1, 0])

    def test_quantum_state_vector_init_from_list(self):
        """Tests QuantumStateVector init from list"""

        quant_state_vec = QuantumStateVector([1, 0])
        self.assertEqual(quant_state_vec.length, 2)
        self.assertEqual(quant_state_vec[0], 1)
        self.assertEqual(quant_state_vec[1], 0)
        self.assertEqual(quant_state_vec.vector, [1, 0])

    def test_quantum_state_vector_init_errors(self):
        """Tests QuantumStateVector init errors"""

        with self.assertRaises(TypeError):
            _ = QuantumStateVector(3.0)
        with self.assertRaises(ValueError):
            _ = QuantumStateVector(0)
        with self.assertRaises(ValueError):
            _ = QuantumStateVector(-1)

        for i in [1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:
            with self.assertRaises(ValueError):
                _ = QuantumStateVector([0] * i)

    def test_quantum_state_vector_from_num_qubits_init(self):
        """Tests QuantumStateVector.from_num_qubits() init"""

        with self.assertRaises(TypeError):
            quant_state_vec = QuantumStateVector().from_num_qubits(3.0)

        quant_state_vec = QuantumStateVector().from_num_qubits(2)
        self.assertEqual(quant_state_vec.length, 4)
        self.assertEqual(quant_state_vec[0], 1)
        self.assertEqual(quant_state_vec[1], 0)
        self.assertEqual(quant_state_vec[2], 0)
        self.assertEqual(quant_state_vec[3], 0)
        self.assertEqual(quant_state_vec.vector, [1, 0, 0, 0])

    def test_quantum_state_vector_get_item(self):
        """Tests QuantumStateVector vector values getter"""

        target_vector = [1, 2, 3, 4, 5, 6, 7, 8]
        quant_state_vec = QuantumStateVector(target_vector)
        for ind, val in enumerate(target_vector):
            self.assertEqual(quant_state_vec[ind], val)
        self.assertEqual(quant_state_vec.vector, target_vector)

        with self.assertRaises(TypeError):
            _ = quant_state_vec[1.0]

    def test_quantum_state_vector_set_item(self):
        """Tests QuantumStateVector vector values setter"""

        target_vector = [1, 2, 3, 4, 5, 6, 7, 8]
        quant_state_vec = QuantumStateVector(3)
        self.assertEqual(quant_state_vec.length, 8)
        self.assertEqual(quant_state_vec.vector, [1, 0, 0, 0, 0, 0, 0, 0])
        for ind, val in enumerate(target_vector):
            quant_state_vec[ind] = val
            self.assertEqual(quant_state_vec[ind], val)
        self.assertEqual(quant_state_vec.vector, target_vector)

        with self.assertRaises(TypeError):
            quant_state_vec[1.0] = 0

    def test_quantrum_state_vector_vector_setter(self):
        """Tests QuantumStateVector vector setter"""

        quant_state_vec = QuantumStateVector([1, 0])
        quant_state_vec.vector = [0, 1]
        quant_state_vec.vector = [1 / np.sqrt(2), 1j / np.sqrt(2)]
        with self.assertRaises(ValueError):
            quant_state_vec.vector = [0, 0, 1]

    def test_quantum_state_vector_to_qiskit(self):
        """Tests QuantumStateVector vector to Qiskit vector conversion"""

        quant_state_vec = QuantumStateVector([1, 0])
        qiskit_state_vector = quant_state_vec.to_qiskit()

        self.assertTrue(isinstance(qiskit_state_vector, QiskitStateVector))
        self.assertEqual(qiskit_state_vector[0], 1)
        self.assertEqual(qiskit_state_vector[1], 0)
