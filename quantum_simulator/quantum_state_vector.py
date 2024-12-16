"Quantum state vector holder module"

import math

# TODO: typing.List is deprecated since Python 3.9. Use list after version update
from typing import Union, List
from qiskit.quantum_info import Statevector as QiskitStateVector


class QuantumStateVector:
    """
    Quantum state vector class

    Qubit Indexing Convention:
        For |ket⟩ vector the first qubit is leftmost. |001⟩ - first and second qubits are in |0⟩ state, third qibit is in |1⟩ state.

        Terms in superposition state are indexed by integer values |0001⟩, |0101⟩ are indexed by 0b1000 (8 in decimal)
        and 0b1010 (10 in decimal) respectively

        |0000⟩ is indexed by 0.
    """

    _vector: List[complex] = None
    "State complex vector"

    _num_qubits: int = None
    "Number of targeted qubits"

    def __init__(self, initializer: Union[list, int] = 1):
        if isinstance(initializer, list):
            # Initialize from the list
            self.from_list(initializer)
        elif isinstance(initializer, int):
            # Initialize from num_qubits
            self.from_num_qubits(initializer)
        else:
            raise TypeError("Wrong initializer type. You must provide either list of amplitudes or number of qubits.")

    @property
    def vector(self) -> List[complex]:
        """QuantumStateVector._vector getter"""
        return self._vector

    @vector.setter
    def vector(self, new_vector: List[complex]) -> None:
        """QuantumStateVector._vector setter"""
        if len(new_vector) != self.length:
            raise ValueError(f"The new vector length ({len(new_vector)}) does not match the expected length ({self.length}).")
        self._vector = new_vector

    @property
    def length(self) -> int:
        """Returns vector length"""
        return 2**self._num_qubits

    def __getitem__(self, key: int) -> complex:
        if not isinstance(key, int):
            raise TypeError("Indexing key must be an integer.")
        return self._vector[key]

    def __setitem__(self, key: int, value: complex) -> None:
        if not isinstance(key, int):
            raise TypeError("Indexing key must be an integer.")
        self._vector[key] = value

    def from_list(self, new_vector: List[complex]):
        """Returns state vector from vector with complex amplitudes"""
        length = len(new_vector)

        # Check if the length is a power of 2
        if not (length > 1 and (length & (length - 1)) == 0):  # Checks if length is power of 2
            raise ValueError("Length of the new vector must be a power of 2.")

        # Update num_qubits based on the length of new vector
        self._num_qubits = round(math.log2(length))
        # Set new vector
        self._vector = new_vector
        return self

    def from_num_qubits(self, num_qubits: int):
        """Returns state vector |0> with desired qubits amount"""
        if not isinstance(num_qubits, int):
            raise TypeError("Number of qubits must be an integer.")
        if num_qubits < 1:
            raise ValueError("Number of qubits must be not less than one.")

        state_vector_length = 2**num_qubits
        vector = [0] * state_vector_length
        # Initialize in the |0⟩ state
        vector[0] = 1
        self._num_qubits = num_qubits
        self._vector = vector
        return self

    def to_qiskit(self) -> QiskitStateVector:
        """Converts QuantumStateVector to QiskitStateVector"""
        qiskit_state_vector = QiskitStateVector(self.vector)
        return qiskit_state_vector
