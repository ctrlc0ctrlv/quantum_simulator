"""Emulator tests module"""

from abc import ABC

import numpy as np
import pytest

from quantum_simulator.custom_quantum_emulator import CustomQuantumEmulator
from quantum_simulator.quantum_operation import OneQubitOperation, TwoQubitsOperation
from quantum_simulator.quantum_state_vector import QuantumStateVector


@pytest.mark.parametrize("emulator", [CustomQuantumEmulator()])
class TestQuantumEmulator(ABC):
    """Abstract QuantumEmulator class. Holds testing fixtures. Tests all supported emulators"""

    # Quantum gates

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

    @pytest.fixture()
    def cnot_gate(self, request):
        """`TwoQubitsOperation` CX (CNOT) gate on `request.param` qubits"""
        return TwoQubitsOperation.CX(request.param)

    @pytest.fixture()
    def cz_gate(self, request):
        """`TwoQubitsOperation` CZ gate on `request.param` qubits"""
        return TwoQubitsOperation.CZ(request.param)

    # Quantum states

    @pytest.fixture()
    def single_qubit_0(self):
        """`QuantumStateVector` |0> state"""
        return QuantumStateVector([1, 0])

    @pytest.fixture()
    def single_qubit_1(self):
        """`QuantumStateVector` |1> state"""
        return QuantumStateVector([0, 1])

    @pytest.fixture()
    def single_qubit_plus(self):
        """`QuantumStateVector` |+> state = (|0> + |1>) / sqrt(2)"""
        return QuantumStateVector([1 / np.sqrt(2), 1 / np.sqrt(2)])

    @pytest.fixture()
    def two_qubit_00(self):
        """`QuantumStateVector` |00> state"""
        return QuantumStateVector([1, 0, 0, 0])

    @pytest.fixture()
    def two_qubit_input_state(self, request):
        """`QuantumStateVector` `requset.param` state"""
        return QuantumStateVector(request.param)


class TestOneQubitOperationSingleQubit(TestQuantumEmulator):
    """Tests single qubit quantum operations on a single qubit using quantum emulator"""

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


class TestOneQubitOperationTwoQubits(TestQuantumEmulator):
    """Tests single qubit quantum operations on a two qubit |00> state using quantum emulator"""

    @pytest.mark.parametrize("pauli_x_gate", (0,), indirect=True)
    def test_apply_pauli_x_first_qubit(self, emulator, two_qubit_00, pauli_x_gate):
        """Tests Pauli-X on first qubit of |00> -> |10>"""
        result = emulator.apply_gate(pauli_x_gate, two_qubit_00)
        expected_result = [0, 1, 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("pauli_x_gate", (1,), indirect=True)
    def test_apply_pauli_x_second_qubit(self, emulator, two_qubit_00, pauli_x_gate):
        """Tests Pauli-X on second qubit of |00> -> |01>"""
        result = emulator.apply_gate(pauli_x_gate, two_qubit_00)
        expected_result = [0, 0, 1, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("pauli_y_gate", (0,), indirect=True)
    def test_apply_pauli_y_first_qubit(self, emulator, two_qubit_00, pauli_y_gate):
        """Tests Pauli-Y on first qubit of |00> -> i|10>"""
        result = emulator.apply_gate(pauli_y_gate, two_qubit_00)
        expected_result = [0, 1j, 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("pauli_y_gate", (1,), indirect=True)
    def test_apply_pauli_y_second_qubit(self, emulator, two_qubit_00, pauli_y_gate):
        """Tests Pauli-Y on second qubit of |00> -> i|01>"""
        result = emulator.apply_gate(pauli_y_gate, two_qubit_00)
        expected_result = [0, 0, 1j, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("pauli_z_gate", (0,), indirect=True)
    def test_apply_pauli_z_first_qubit(self, emulator, two_qubit_00, pauli_z_gate):
        """Tests Pauli-Z on first qubit of |00> -> |00>"""
        result = emulator.apply_gate(pauli_z_gate, two_qubit_00)
        expected_result = [1, 0, 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("pauli_z_gate", (1,), indirect=True)
    def test_apply_pauli_z_second_qubit(self, emulator, two_qubit_00, pauli_z_gate):
        """Tests Pauli-Z on second qubit of |00> -> |00>"""
        result = emulator.apply_gate(pauli_z_gate, two_qubit_00)
        expected_result = [1, 0, 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("hadamard_gate", (0,), indirect=True)
    def test_apply_hadamard_first_qubit(self, emulator, two_qubit_00, hadamard_gate):
        """Tests T on first qubit of |00> -> (|00> + |10>) / sqrt(2)"""
        result = emulator.apply_gate(hadamard_gate, two_qubit_00)
        expected_result = [1 / np.sqrt(2), 1 / np.sqrt(2), 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("hadamard_gate", (1,), indirect=True)
    def test_apply_hadamard_second_qubit(self, emulator, two_qubit_00, hadamard_gate):
        """Tests T on second qubit of |00> -> (|00> + |01>) / sqrt(2)"""
        result = emulator.apply_gate(hadamard_gate, two_qubit_00)
        expected_result = [1 / np.sqrt(2), 0, 1 / np.sqrt(2), 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("t_gate", (0,), indirect=True)
    def test_apply_t_first_qubit(self, emulator, two_qubit_00, t_gate):
        """Tests T on first qubit of |00> -> |00>"""
        result = emulator.apply_gate(t_gate, two_qubit_00)
        expected_result = [1, 0, 0, 0]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize("t_gate", (1,), indirect=True)
    def test_apply_t_second_qubit(self, emulator, two_qubit_00, t_gate):
        """Tests T on second qubit of |00> -> |00>"""
        result = emulator.apply_gate(t_gate, two_qubit_00)
        expected_result = [1, 0, 0, 0]
        assert np.allclose(result.vector, expected_result)


class TestTwoQubitOperationTwoQubits(TestQuantumEmulator):
    """Tests two qubits quantum operations on a two qubit |00> state using quantum emulator"""

    @pytest.mark.parametrize(["two_qubit_input_state", "cnot_gate"], [([0, 0, 1, 0], [0, 1])], indirect=True)
    def test_apply_cnot(self, emulator, two_qubit_input_state, cnot_gate):
        """Tests CNOT on state |01> -> |11>"""
        result = emulator.apply_gate(cnot_gate, two_qubit_input_state)
        expected_result = [0, 0, 0, 1]
        assert np.allclose(result.vector, expected_result)

    @pytest.mark.parametrize(["two_qubit_input_state", "cz_gate"], [([0, 0, 0, 1], [0, 1])], indirect=True)
    def test_apply_cz(self, emulator, two_qubit_input_state, cz_gate):
        """Tests CZ on state |11> -> -|11>"""
        result = emulator.apply_gate(cz_gate, two_qubit_input_state)
        expected_result = [0, 0, 0, -1]
        assert np.allclose(result.vector, expected_result)
