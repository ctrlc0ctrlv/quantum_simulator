"""Abstract quantum emulator module"""

from abc import ABC, abstractmethod

from quantum_simulator.quantum_circuit import QuantumCircuit
from quantum_simulator.quantum_operation import QuantumOperation
from quantum_simulator.quantum_state_vector import QuantumStateVector


class AbstractQuantumEmulator(ABC):
    """Abstract quantum emulator class"""

    @abstractmethod
    def apply_gate(self, operation: QuantumOperation, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum operation to a given state vector"""

    @abstractmethod
    def apply_circuit(self, circuit: QuantumCircuit, state_vector: QuantumStateVector) -> QuantumStateVector:
        """Applies quantum circuit to a given state vector"""

    # TODO clarify function arguments
    @abstractmethod
    def execute(self, circuit: QuantumCircuit):
        """Executes given circuit"""

    # TODO clarify function arguments
    @abstractmethod
    def execute_shots(self, circuit: QuantumCircuit, n_shots: int):
        """Executes shots using given circuit"""
