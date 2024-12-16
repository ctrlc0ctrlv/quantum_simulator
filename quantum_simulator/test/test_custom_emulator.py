"""Custom emulator tests module"""

import numpy as np
import pytest

from quantum_simulator.quantum_state_vector import QuantumStateVector
from quantum_simulator.custom_quantum_emulator import CustomQuantumEmulator
from quantum_simulator.quantum_operation import OneQubitOperation


class TestCustomOperationSingleQubit:
    """Tests quantum operations on a single qubit using custom quantum emulator"""

    @pytest.fixture()
    def emulator(self):
        """Returns `CustomQuantumEmulator` instance"""
        return CustomQuantumEmulator()

    @pytest.fixture()
    def single_qubit_0(self):
        """`QuantumStateVector` |0> state"""
        return QuantumStateVector(1)

    @pytest.fixture()
    def single_qubit_1(self):
        """`QuantumStateVector` |1> state"""
        return QuantumStateVector([0, 1])

    @pytest.fixture()
    def single_qubit_plus(self):
        """`QuantumStateVector` |+> state = (|0> + |1>) / sqrt(2)"""
        return QuantumStateVector([1 / np.sqrt(2), 1 / np.sqrt(2)])

    @pytest.fixture()
    def pauli_x_gate(self):
        """`OneQubitOperation` Pauli X gate"""
        return OneQubitOperation.X()

    @pytest.fixture()
    def pauli_y_gate(self):
        """`OneQubitOperation` Pauli Y gate"""
        return OneQubitOperation.Y()

    @pytest.fixture()
    def pauli_z_gate(self):
        """`OneQubitOperation` Pauli Z gate"""
        return OneQubitOperation.Z()

    @pytest.fixture()
    def hadamard_gate(self):
        """`OneQubitOperation` H gate"""
        return OneQubitOperation.H()

    @pytest.fixture()
    def t_gate(self):
        """`OneQubitOperation` T gate"""
        return OneQubitOperation.T()

    def test_pauli_x(self, emulator, pauli_x_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli X operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_0).vector, [0, 1])
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_1).vector, [1, 0])

    def test_pauli_y(self, emulator, pauli_y_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli Y operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_0).vector, [0, 1j])
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_1).vector, [-1j, 0])

    def test_pauli_z(self, emulator, pauli_z_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli Z operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_1).vector, [0, -1])

    def test_hadamard(self, emulator, hadamard_gate, single_qubit_0, single_qubit_1):
        """Tests H operation execution"""
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_0).vector, [1 / np.sqrt(2), 1 / np.sqrt(2)])
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_1).vector, [1 / np.sqrt(2), -1 / np.sqrt(2)])

    def test_t_gate(self, emulator, t_gate, single_qubit_0, single_qubit_1):
        """Tests T operation execution"""
        t_phase = np.exp(1j * np.pi / 4)
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_1).vector, [0, t_phase])

    def test_superposition(self, emulator, pauli_x_gate, pauli_z_gate, single_qubit_plus):
        """Tests operations execution on a |+> state"""
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_plus).vector, single_qubit_plus.vector)
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_plus).vector, [1 / np.sqrt(2), -1 / np.sqrt(2)])
