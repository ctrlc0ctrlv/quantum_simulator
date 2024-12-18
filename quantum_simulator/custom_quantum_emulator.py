"""Custom quantum emulator module"""

# TODO: typing.List is deprecated since Python 3.9. Use list after version update
from typing import List

from quantum_simulator.abstract_quantum_emulator import AbstractQuantumEmulator
from quantum_simulator.quantum_circuit import QuantumCircuit
from quantum_simulator.quantum_operation import QuantumOperation
from quantum_simulator.quantum_state_vector import QuantumStateVector


class CustomQuantumEmulator(AbstractQuantumEmulator):
    """Custom quantum emulator class"""

    def __init__(self):
        pass

    def apply_gate(self, operation: QuantumOperation, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum operation to a given state vector"""
        target_qubits = operation.target_qubits

        if any(id >= state_vector.num_qubits for id in target_qubits):
            # raise OperandOutOfBoundsError(operation, state_vector.num_qubits)
            raise ValueError()

        output = None
        if len(target_qubits) == 1:
            output = self._apply1Q(state_vector, operation)
        elif len(target_qubits) == 2:
            output = self._apply2Q(state_vector, operation)
        else:
            # raise UnsupportedNumberOfQubits(operation)
            raise ValueError()
        return output

    def apply_circuit(self, circuit: QuantumCircuit, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum circuit to a given state vector"""
        if circuit.width != state_vector.num_qubits:
            raise ValueError("state_vector and circuit size mismatch")

        output = state_vector
        for gate in circuit.gates:
            output = self.apply_gate(gate, output)
        return output

    # TODO clarify function arguments
    def execute(self, circuit: QuantumCircuit):
        """Executes given circuit"""

    # TODO clarify function arguments
    def execute_shots(self, circuit: QuantumCircuit, n_shots: int):
        """Executes shots using given circuit"""

    @staticmethod
    def _replace_bit(num: int, loc: int, val: bool) -> int:
        """Sets bit located at `loc` in `num` to `val`"""
        if val:
            return num | (1 << loc)
        return num & (~(1 << loc))

    @staticmethod
    def _replace_bits(num: int, locs: List[int], vals: List[bool]) -> int:
        """in 'num', set bits located at 'locs' to values provided in 'vals'"""
        assert len(locs) == len(vals), f"Number indeces != number of values, got {len(locs)} != {len(vals)}"
        for loc, val in zip(locs, vals):
            num = CustomQuantumEmulator._replace_bit(num, loc, val)
        return num

    @staticmethod
    def _apply1Q(state: QuantumStateVector, operation: QuantumOperation) -> QuantumStateVector:
        """Applies 1-qubit gate `operation` to a state vector `state`"""
        target_qubit_ind = operation.target_qubits[0]
        output_state = QuantumStateVector([0] * state.length)
        matrix = operation.matrix

        for state_ind in range(output_state.length):
            j_k = (state_ind >> target_qubit_ind) & 1
            for i_k in range(2):
                running_index = CustomQuantumEmulator._replace_bit(state_ind, target_qubit_ind, i_k)
                output_state[state_ind] += state[running_index] * matrix[j_k, i_k]
        return output_state

    @staticmethod
    def _apply2Q(state: QuantumStateVector, operation: QuantumOperation) -> QuantumStateVector:
        """Applies 1-qubit gate `operation` to a state vector `state`"""
        qubit1_index, qubit2_index = operation.target_qubits
        output_state = QuantumStateVector([0] * state.length)
        matrix = operation.matrix

        for state_ind in range(output_state.length):
            j_k1 = (state_ind >> qubit1_index) & 1
            j_k2 = (state_ind >> qubit2_index) & 1
            bra = int(f"{j_k2}{j_k1}", base=2)
            for i_k1 in range(2):
                for i_k2 in range(2):
                    running_index = CustomQuantumEmulator._replace_bits(state_ind, [qubit1_index, qubit2_index], [i_k1, i_k2])
                    ket = int(f"{i_k2}{i_k1}", base=2)
                    output_state[state_ind] += state[running_index] * matrix[bra, ket]
        return output_state
