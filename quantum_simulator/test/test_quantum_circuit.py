"""Random generator tests module"""

from unittest import TestCase

import pytest

from quantum_simulator.quantum_circuit import QuantumCircuit


@pytest.mark.quant_circuit
class TestQuantumCircuit(TestCase):
    """RandomGenerator tests class"""

    def test_quantum_circuit(self):
        """Tests QuantumCircuit init"""
        quantum_circuit = QuantumCircuit(num_qubits=1, depth=3, seed=27)
        self.assertEqual(quantum_circuit.seed, 27)
        self.assertEqual(quantum_circuit.depth, 3)
        self.assertEqual(quantum_circuit.num_qubits, 1)
