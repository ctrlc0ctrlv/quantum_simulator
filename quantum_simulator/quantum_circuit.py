"""Quantum circuit module"""

from quantum_simulator.quantum_operation import OneQubitOperation, TwoQubitsOperation
from quantum_simulator.random_generator import RandomGenerator


class QuantumCircuit:
    """Quantum circuit class"""

    _width: int
    "Number of qubits in circuit"

    _depth: int
    "Max number of gates"

    weight_2q: float
    "2-qubits operation weight"

    seed: int
    "Random seed"

    random_generator: RandomGenerator = None
    "Random unitary gates generator"

    gate_layers: list = None
    "Circuit gate layers - `[(list_of_layer_gates, set_of_targeted_qubits)]`"

    def __init__(self, width: int, depth: int, weight_2q: float, seed: int = 27):
        self._width = width
        self._depth = depth
        self.weight_2q = weight_2q
        self.seed = seed
        self.random_generator = RandomGenerator(seed=self.seed)
        self.gate_layers = []

    @property
    def depth(self):
        """Max number of gates read-only property"""
        return self._depth

    @property
    def width(self):
        """Number of qubits in circuit read-only property"""
        return self._width
