"""Custom quantum emulator module"""

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
        pass

    def apply_circuit(self, circuit: QuantumCircuit, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum circuit to a given state vector"""
        pass

    # TODO clarify function arguments
    def execute(self, circuit: QuantumCircuit):
        """Executes given circuit"""
        pass

    # TODO clarify function arguments
    def execute_shots(self, circuit: QuantumCircuit, n_shots: int):
        """Executes shots using given circuit"""
        pass
