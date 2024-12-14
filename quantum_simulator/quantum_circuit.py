"""Quantum circuit module"""

from quantum_simulator.random_generator import RandomGenerator


class QuantumCircuit:
    """Quantum circuit class"""

    num_qubits: int
    "Number of qubits in circuit"

    depth: int
    "Max number of gates"

    seed: int
    "Random seed"

    random_generator: RandomGenerator = None
    "Random unitary gates generator"

    def __init__(self, num_qubits: int, depth: int, seed: int = 27):
        self.num_qubits = num_qubits
        self.depth = depth
        self.seed = seed
        self.random_generator = RandomGenerator(seed=self.seed)
