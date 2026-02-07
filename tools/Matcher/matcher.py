import numpy as np
from munkres import Munkres
import networkx as nx


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

    def max_weight_matching_same_group(self) -> list[tuple[int, int]]:
        """
        Same-group pairing: maximize sum of scores over disjoint pairs (no cycles).
        Use this instead of hungarian() for FF/MM so the result is always a matching.
        Input matrix should be n×n symmetric; returns [(i, j), ...] with i < j.
        """
        n, _ = self.m.shape
        G = nx.Graph()
        for i in range(n):
            for j in range(i + 1, n):
                w = float(self.m[i, j])
                if w > 0:
                    G.add_edge(i, j, weight=w)
        raw = nx.max_weight_matching(G, maxcardinality=False, weight="weight")
        return [tuple(sorted(e)) for e in raw]