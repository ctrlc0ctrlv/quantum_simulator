"""Abstract quantum operation and 1-2-qubit operation module"""

from abc import ABC, abstractmethod

import numpy as np


class QuantumOperation(ABC):
    """Abstract quantum operation class"""

    _matrix: np.ndarray
    _target_qubits: list

    __I: np.ndarray
    "Pauli I operation matrix"

    @abstractmethod
    def __init__(self, matrix: np.ndarray, target_qubits: list):
        super().__init__()
        if not isinstance(matrix, np.ndarray):
            raise TypeError("Value of matrix should be a np.ndarray")
        if not self.__matrix_size_is_ok(matrix):
            raise ValueError(f"Wrong matrix size for {self.__class__.__name__}")
        if not isinstance(target_qubits, list):
            raise TypeError("Value of target_qubits should be a list")
        if not self.__class__._target_qubits_size_is_ok(target_qubits):
            raise ValueError(
                f"Wrong target qubits size: should be {round(np.log2(self.__class__.target_matrix_size()))}, got {len(target_qubits)}",
            )
        self._matrix = matrix
        self._target_qubits = target_qubits

    @property
    def matrix(self) -> np.ndarray:
        """Returns matrix corresponding to quantum operation"""
        return self._matrix

    @property
    def target_qubits(self) -> list:
        """Returns list of targeted qubits"""
        return self._target_qubits

    @staticmethod
    @abstractmethod
    def target_matrix_size() -> int:
        "Target matrix size"

    def __matrix_size_is_ok(self, matrix):
        if matrix.shape[0] != self.__class__.target_matrix_size() or matrix.shape[1] != self.__class__.target_matrix_size():
            return False
        return True

    @classmethod
    def _target_qubits_size_is_ok(cls, target_qubits):
        if 2 ** len(target_qubits) != cls.target_matrix_size():
            return False
        return True

    @classmethod
    def I(cls):
        """Identity one-qubit operation"""
        return cls(
            np.eye(cls.target_matrix_size()),
            [None for x in range(round(np.log2(cls.target_matrix_size())))],
        )


class OneQubitOperation(QuantumOperation):
    """Single qubit quantum operation class"""

    __X: np.ndarray = np.array([[0, 1], [1, 0]])
    "Pauli X operation matrix"

    __Y: np.ndarray = np.array([[0, -1j], [1j, 0]])
    "Pauli Y operation matrix"

    __Z: np.ndarray = np.array([[1, 0], [0, -1]])
    "Pauli Z operation matrix"

    def __init__(self, matrix, target_qubits):
        super().__init__(matrix, target_qubits)

    @staticmethod
    def target_matrix_size():
        return 2

    @staticmethod
    def X(target_qubits: list = None):
        """X Pauli operation"""
        if target_qubits is None:
            target_qubits = [0]
        return OneQubitOperation(OneQubitOperation.__X, target_qubits)

    @staticmethod
    def Y(target_qubits: list = None):
        """Y Pauli operation"""
        if target_qubits is None:
            target_qubits = [0]
        return OneQubitOperation(OneQubitOperation.__Y, target_qubits)

    @staticmethod
    def Z(target_qubits: list = None):
        """Z Pauli operation"""
        if target_qubits is None:
            target_qubits = [0]
        return OneQubitOperation(OneQubitOperation.__Z, target_qubits)


class TwoQubitsOperation(QuantumOperation):
    """Two qubits quantum operation class"""

    __CX: np.ndarray = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    "CX operation matrix"

    __CZ: np.ndarray = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
    "CZ operation matrix"

    def __init__(self, matrix, target_qubits):
        super().__init__(matrix, target_qubits)

    @staticmethod
    def target_matrix_size():
        return 4

    @staticmethod
    def CX(target_qubits: list = None):
        """CX operation"""
        if target_qubits is None:
            target_qubits = [0, 1]
        return TwoQubitsOperation(TwoQubitsOperation.__CX, target_qubits)

    @staticmethod
    def CZ(target_qubits: list = None):
        """CZ operation"""
        if target_qubits is None:
            target_qubits = [0, 1]
        return TwoQubitsOperation(TwoQubitsOperation.__CZ, target_qubits)
