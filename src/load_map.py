from typing import List, Tuple

import cv2
import numpy as np

from src.path_finder import PathFinder


class LoadMap:
    path_finder: PathFinder

    def __init__(self, file: str):
        self.map_name: str = file
        self.map = self.load_map()
        self.speed: int = 100
        self.combin = {1: (0, 0, 0), 0: (255, 255, 255), 2: (0, 0, 255), 3: (0, 255, 0)}
        self.combin_text = {2: "START", 3: "GOAL"}
        self.actions = ["UP", "LEFT", "RIGHT"]
        self.get_speed_by_map()
        self.map: List[List[int]] = self.transform_map()

    def load_map(self) -> List[List[int]]:
        return cv2.imread(self.map_name, cv2.IMREAD_UNCHANGED)

    def get_speed(self) -> int:
        return self.speed

    def get_speed_by_map(self) -> None:
        for i in range(len(self.map[0])):
            if tuple(self.map[0][i]) != (255, 0, 0):
                self.speed = self.speed // i
                break

    def transform_map(self) -> List[List[int]]:
        map = []
        for i in range(len(self.map)):
            map.append([])
            for j in range(len(self.map[i])):
                match tuple(self.map[i][j]):
                    case (255, 255, 255):
                        map[i].append(0)
                    case (0, 0, 0) | (1, 0, 0) | (0, 1, 0) | (0, 0, 1):
                        map[i].append(1)
                    case (0, 0, 255):
                        map[i].append(2)
                    case (0, 255, 0):
                        map[i].append(3)
                    case _:
                        map[i].append(0)

        return map

    def get_map(self) -> List[List[int]]:
        return self.map

    def get_start_coordinates(self) -> tuple[None, None] | Tuple[int, int]:
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 2:
                    return j, i
        return None, None

    def get_goal_coordinates(self) -> List:
        goal = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 3:
                    goal.append((j, i))
        return goal

    def get_optimal_actions(self) -> List[List[str]]:
        actions = []
        start = self.get_start_coordinates()
        goals = self.get_goal_coordinates()
        self.clean_map()
        self.path_finder = PathFinder(self.map)
        actions.append(self.get_actions(start, goals[0], True))
        for i in range(1, len(goals)):
            actions.append(self.get_actions(goals[i - 1], goals[i], False))
            actions.append(self.get_actions(goals[-1], start, False))

        return actions

    def get_actions(self, start: Tuple[int, int], goal: Tuple[int, int], is_start: bool) -> List[str]:
        way = self.path_finder.create_path(start, goal)
        actions_simplified = []
        actions = []
        last_turn = "UP"
        for i in range(1, len(way) - 1):
            if way[i + 1][0] == way[i][0] - 1:
                actions.append("LEFT")
            elif way[i + 1][0] == way[i][0] + 1:
                actions.append("RIGHT")
            elif way[i + 1][1] == way[i][1] - 1:
                actions.append("UP")
            elif way[i + 1][1] == way[i][1] + 1:
                actions.append("DOWN")

        if not is_start:
            actions_simplified.append("LEFT")
            actions_simplified.append("LEFT")
        for act in actions:
            if act != last_turn:
                match act:
                    case "LEFT":
                        match last_turn:
                            case "UP":
                                actions_simplified.append("LEFT")
                            case "DOWN":
                                actions_simplified.append("RIGHT")
                            case "RIGHT":
                                actions_simplified.append("LEFT")
                                actions_simplified.append("LEFT")
                    case "RIGHT":
                        match last_turn:
                            case "UP":
                                actions_simplified.append("RIGHT")
                            case "DOWN":
                                actions_simplified.append("LEFT")
                            case "LEFT":
                                actions_simplified.append("RIGHT")
                                actions_simplified.append("RIGHT")
                    case "UP":
                        match last_turn:
                            case "LEFT":
                                actions_simplified.append("RIGHT")
                            case "DOWN":
                                actions_simplified.append("LEFT")
                                actions_simplified.append("LEFT")
                            case "RIGHT":
                                actions_simplified.append("LEFT")
                    case "DOWN":
                        match last_turn:
                            case "UP":
                                actions_simplified.append("LEFT")
                                actions_simplified.append("LEFT")
                            case "LEFT":
                                actions_simplified.append("RIGHT")
                            case "RIGHT":
                                actions_simplified.append("LEFT")

                last_turn = act
            else:
                actions_simplified.append("UP")

        return actions_simplified

    def clean_map(self):
        widths = []
        for i in range(len(self.map)):
            widths.append(len(self.map[i]))
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] != 0:
                    self.map[i][j] = 1
