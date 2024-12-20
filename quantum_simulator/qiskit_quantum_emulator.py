"""Qiskit quantum emulator module"""

from qiskit.circuit.library import UnitaryGate as QiskitUnitaryGate

from quantum_simulator.abstract_quantum_emulator import AbstractQuantumEmulator
from quantum_simulator.quantum_circuit import QuantumCircuit
from quantum_simulator.quantum_operation import QuantumOperation
from quantum_simulator.quantum_state_vector import QuantumStateVector


class QiskitQuantumEmulator(AbstractQuantumEmulator):
    """Qiskit quantum emulator class"""

    def __init__(self):
        pass

    def apply_gate(self, operation: QuantumOperation, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum operation to a given state vector"""
        qiskit_state_vector = state_vector.to_qiskit()
        qiskit_gate = QiskitUnitaryGate(operation.matrix)
        qiskit_evolved = qiskit_state_vector.evolve(qiskit_gate, qargs=operation.target_qubits)
        output = QuantumStateVector(qiskit_evolved.data.tolist())
        return output

    def apply_circuit(self, circuit: QuantumCircuit, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum circuit to a given state vector"""
        if circuit.width != state_vector.num_qubits:
            raise ValueError("state_vector and circuit size mismatch")

        qiskit_circuit = circuit.to_qiskit()
        qiskit_state_vector = state_vector.to_qiskit()
        qiskit_modified = qiskit_state_vector.evolve(qiskit_circuit)
        output = QuantumStateVector(qiskit_modified.data.tolist())
        return output

    # TODO clarify function arguments
    def execute(self, circuit: QuantumCircuit):
        """Executes given circuit"""

    # TODO clarify function arguments
    def execute_shots(self, circuit: QuantumCircuit, n_shots: int):
        """Executes shots using given circuit"""
