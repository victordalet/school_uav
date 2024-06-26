from typing import List
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class PathFinder:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)

    def create_path(
        self, launch: tuple[int, int], goal: tuple[int, int]
    ) -> List[tuple[int, int]]:
        start = self.grid.node(launch[0], launch[1])
        end = self.grid.node(goal[0], goal[1])
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        return path
