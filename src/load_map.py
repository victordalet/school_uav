from typing import List, Tuple

import cv2


class LoadMap:
    def __init__(self, file: str):
        self.map_name: str = file
        self.map = self.load_map()
        self.combin = {1: (0, 0, 0), 0: (255, 255, 255), 2: (255, 0, 0), 3: (0, 255, 0), 4: (0, 0, 255)}
        self.combin_text = {2: "START", 3: "GOAL"}
        self.actions = ["UP", "LEFT", "RIGHT"]
        self.map: List[List[int]] = self.transform_map()

    def load_map(self) -> List[List[int]]:
        map = cv2.imread(self.map_name)
        return map

    def transform_map(self) -> List[List[int]]:
        map = []
        for i in range(len(self.map)):
            map.append([])
            for j in range(len(self.map[i])):
                map[i].append(self.combin[self.map[i][j][0]])
        return map

    def get_map(self):
        return self.map

    def get_start_coordinates(self) -> tuple[None, None] | Tuple[int, int]:
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == self.combin[2]:
                    return i, j
        return None, None

    def get_goal_coordinates(self) -> List:
        goal = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == self.combin[3]:
                    goal.append((i, j))
        return goal

    def get_optimal_actions(self) -> List[List[str]]:
        actions = []
        start = self.get_start_coordinates()
        goals = self.get_goal_coordinates()
        actions += self.get_actions(start, goals[0])
        for i in range(1, len(goals)):
            actions += self.get_actions(goals[i - 1], goals[i])
        actions.append(self.get_actions(goals[-1], start))

        return actions

    def get_actions(self, start, goal) -> List[str]:

        actions = []
        while start != goal:
            next = self.get_next(start, goal)
            actions.append(next)
            if next == "RIGHT":
                start = (start[0], start[1] + 1)
            elif next == "LEFT":
                start = (start[0], start[1] - 1)
            elif next == "DOWN":
                start = (start[0] + 1, start[1])
            else:
                start = (start[0] - 1, start[1])
        return actions

    @staticmethod
    def get_next(start, goal):
        if start[0] == goal[0]:
            if start[1] < goal[1]:
                return "RIGHT"
            else:
                return "LEFT"
        elif start[0] < goal[0]:
            return "DOWN"
        else:
            return "UP"
