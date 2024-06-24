import sys

import cv2

from src.const import SPEED_FORWARD_UAV, SPEED_LEFT_UAV, SPEED_RIGHT_UAV
from src.discoverer_map import DiscovererMap
from src.load_map import LoadMap
from src.student import Student
from src.uav import UAV


class Run:

    def __init__(self):
        self.config: str = sys.argv[1]
        self.map: LoadMap = LoadMap(sys.argv[2])
        self.student_detector: Student = Student()
        self.way = self.map.get_optimal_actions()
        self.index_way: int = 0
        self.index_action_by_way: int = 0
        self.run: bool = True
        self.uav: UAV = UAV()
        self.discover_map: DiscovererMap = DiscovererMap()
        self.launch()

    def launch(self) -> None:
        self.uav.take_off()
        cap = cv2.VideoCapture(0)
        while self.run:
            _, img = cap.read()

            self.verif_index_navigation(img)
            self.verif_depth_environment(img)
            self.navigate()

    def verif_index_navigation(self, img: cv2.typing.MatLike) -> None:
        if self.index_action_by_way == len(self.way[self.index_way]):
            self.index_way += 1
            self.index_action_by_way = 0
            if self.config == "count":
                self.student_detector.search_number_total_students(img)

        if self.index_way == len(self.way):
            self.student_detector.get_result_csv()
            self.run = False

    def navigate(self):
        if self.way[self.index_way][self.index_action_by_way] == "UP":
            self.uav.forward(SPEED_FORWARD_UAV)
        elif self.way[self.index_way][self.index_action_by_way] == "LEFT":
            self.uav.left(SPEED_LEFT_UAV)
        elif self.way[self.index_way][self.index_action_by_way] == "RIGHT":
            self.uav.right(SPEED_RIGHT_UAV)
        self.index_action_by_way += 1

    def verif_depth_environment(self, img: cv2.typing.MatLike) -> None:
        depth = self.discover_map.transform_depth_map(img)
        point = self.discover_map.get_point_depth(depth)
        self.uav.orientate(point, img.shape[1], img.shape[0])


if __name__ == "__main__":
    Run()
