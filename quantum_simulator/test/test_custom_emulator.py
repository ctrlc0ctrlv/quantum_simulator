"""Custom emulator tests module"""

from abc import ABC

import numpy as np
import pytest

from quantum_simulator.quantum_state_vector import QuantumStateVector
from quantum_simulator.custom_quantum_emulator import CustomQuantumEmulator
from quantum_simulator.quantum_operation import OneQubitOperation


class TestCustomQuantumEmulator(ABC):
    """Abstract CustomQuantumEmulator class. Holds testing fixtures"""

    @pytest.fixture()
    def emulator(self):
        """Returns `CustomQuantumEmulator` instance"""
        return CustomQuantumEmulator()

    @pytest.fixture()
    def pauli_x_gate(self, request):
        """`OneQubitOperation` Pauli X gate on `request.param` qubit"""
        return OneQubitOperation.X([request.param])

    @pytest.fixture()
    def pauli_y_gate(self, request):
        """`OneQubitOperation` Pauli Y gate on `request.param` qubit"""
        return OneQubitOperation.Y([request.param])

    @pytest.fixture()
    def pauli_z_gate(self, request):
        """`OneQubitOperation` Pauli Z gate on `request.param` qubit"""
        return OneQubitOperation.Z([request.param])

    @pytest.fixture()
    def hadamard_gate(self, request):
        """`OneQubitOperation` H gate on `request.param` qubit"""
        return OneQubitOperation.H([request.param])

    @pytest.fixture()
    def t_gate(self, request):
        """`OneQubitOperation` T gate on `request.param` qubit"""
        return OneQubitOperation.T([request.param])


class TestCustomQuantumEmulatorSingleQubit(TestCustomQuantumEmulator):
    """Tests quantum operations on a single qubit using custom quantum emulator"""

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

    @pytest.mark.parametrize("pauli_x_gate", (0,), indirect=True)
    def test_pauli_x(self, emulator, pauli_x_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli X operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_0).vector, [0, 1])
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_1).vector, [1, 0])

    @pytest.mark.parametrize("pauli_y_gate", (0,), indirect=True)
    def test_pauli_y(self, emulator, pauli_y_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli Y operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_0).vector, [0, 1j])
        assert np.allclose(emulator.apply_gate(pauli_y_gate, single_qubit_1).vector, [-1j, 0])

    @pytest.mark.parametrize("pauli_z_gate", (0,), indirect=True)
    def test_pauli_z(self, emulator, pauli_z_gate, single_qubit_0, single_qubit_1):
        """Tests Pauli Z operation execution"""
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_1).vector, [0, -1])

    @pytest.mark.parametrize("hadamard_gate", (0,), indirect=True)
    def test_hadamard(self, emulator, hadamard_gate, single_qubit_0, single_qubit_1):
        """Tests H operation execution"""
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_0).vector, [1 / np.sqrt(2), 1 / np.sqrt(2)])
        assert np.allclose(emulator.apply_gate(hadamard_gate, single_qubit_1).vector, [1 / np.sqrt(2), -1 / np.sqrt(2)])

    @pytest.mark.parametrize("t_gate", (0,), indirect=True)
    def test_t_gate(self, emulator, t_gate, single_qubit_0, single_qubit_1):
        """Tests T operation execution"""
        t_phase = np.exp(1j * np.pi / 4)
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_0).vector, [1, 0])
        assert np.allclose(emulator.apply_gate(t_gate, single_qubit_1).vector, [0, t_phase])

    @pytest.mark.parametrize(["pauli_x_gate", "pauli_z_gate"], [(0, 0)], indirect=True)
    def test_superposition(self, emulator, pauli_x_gate, pauli_z_gate, single_qubit_plus):
        """Tests operations execution on a |+> state"""
        assert np.allclose(emulator.apply_gate(pauli_x_gate, single_qubit_plus).vector, single_qubit_plus.vector)
        assert np.allclose(emulator.apply_gate(pauli_z_gate, single_qubit_plus).vector, [1 / np.sqrt(2), -1 / np.sqrt(2)])
