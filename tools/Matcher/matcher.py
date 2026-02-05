import numpy as np
from munkres import Munkres


class Matcher:
    def __init__(self, m: np.ndarray):
        self.m = m
        self.munkers = Munkres()

    def prepareMatrix(self) -> np.ndarray:
        if self.m.shape[0] == self.m.shape[1]:
            return self.m
        padded = np.zeros((max(self.m.shape), max(self.m.shape)), dtype=int)
        padded[:self.m.shape[0], :self.m.shape[1]] = self.m
        self.m = padded
        return self.m
    
    def calculate_cost_matrix(self) -> np.ndarray:
        return np.max(self.m) - self.m

    def hungarian(self) -> list[tuple[int, int]]:
        self.prepareMatrix()
        cost = self.calculate_cost_matrix()
        indexes = self.munkers.compute(cost)
        return indexes