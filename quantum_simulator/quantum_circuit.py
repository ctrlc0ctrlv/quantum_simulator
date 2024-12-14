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
    
    def generate_gates_and_unite(self) -> None:
        """
        Generates random gates.

        Also compresses the layer, so that each layer has as many simultaneous operations as possible
        """
        for _ in range(self.depth):
            rand_num = self.random_generator.rand()
            if rand_num >= self.weight_2q or self.width == 1:
                q = self.random_generator.rand_int() % self.width
                U = self.random_generator.rand_unitary(mode="1q")
                gate = OneQubitOperation(U, [q])
                q1, q2 = q, q
            else:
                q1 = self.random_generator.rand_int() % self.width
                q2 = self.random_generator.rand_int() % self.width
                while q2 == q1:
                    q2 = self.random_generator.rand_int() % self.width
                U = self.random_generator.rand_unitary(mode="2q")
                gate = TwoQubitsOperation(U, [q1, q2])

            # compress gate layers if possible
            idx = len(self.gate_layers) - 1
            while idx >= 0 and q1 not in self.gate_layers[idx][1] and q2 not in self.gate_layers[idx][1]:
                idx -= 1
            idx += 1
            if idx == len(self.gate_layers):
                self.gate_layers.append(([gate], {q1, q2}))
            else:
                self.gate_layers[idx][0].append(gate)
                self.gate_layers[idx][1].add(q1)
                self.gate_layers[idx][1].add(q2)
