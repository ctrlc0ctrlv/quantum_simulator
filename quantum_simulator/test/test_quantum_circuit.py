"""Random generator tests module"""

from unittest import TestCase

import pytest

from quantum_simulator.quantum_circuit import QuantumCircuit


@pytest.mark.quant_circuit
class TestQuantumCircuit(TestCase):
    """RandomGenerator tests class"""

    def test_quantum_circuit(self):
        """Tests QuantumCircuit init"""
        quantum_circuit = QuantumCircuit(width=1, depth=3, weight_2q=1 / 3, seed=27)
        self.assertEqual(quantum_circuit.seed, 27)
        self.assertEqual(quantum_circuit.depth, 3)
        self.assertAlmostEqual(quantum_circuit.weight_2q, 1 / 3)
        self.assertEqual(quantum_circuit.width, 1)

    def test_generate_gates_and_unite(self):
        """Tests QuantumCircuit.generate_gates_and_unite() function"""
        # only 1q-gates (no optimizations)
        for seed in range(100):
            quantum_circuit = QuantumCircuit(width=1, depth=100, weight_2q=0.5, seed=seed)
            quantum_circuit.generate_gates_and_unite()
            self.assertEqual(len(quantum_circuit.gate_layers), quantum_circuit.depth)
            for _, target_qubits in quantum_circuit.gate_layers:
                self.assertEqual(target_qubits, {0})

        # only 2q-gates (no optimizations)
        for seed in range(100):
            quantum_circuit = QuantumCircuit(width=2, depth=100, weight_2q=1, seed=seed)
            quantum_circuit.generate_gates_and_unite()
            self.assertEqual(len(quantum_circuit.gate_layers), quantum_circuit.depth)
            for _, target_qubits in quantum_circuit.gate_layers:
                self.assertEqual(target_qubits, {0, 1})

        # 1q gates on wide circuit (optimizations)
        for seed in range(100):
            quantum_circuit = QuantumCircuit(width=100, depth=100, weight_2q=0, seed=seed)
            quantum_circuit.generate_gates_and_unite()
            self.assertLessEqual(len(quantum_circuit.gate_layers), quantum_circuit.depth)

            last_layer_target = quantum_circuit.gate_layers[-1][1]
            # ensure last layer qubits cannot be moved lower
            for _, target_qubits in quantum_circuit.gate_layers:
                self.assertTrue(last_layer_target.issubset(target_qubits))
