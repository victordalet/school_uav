from typing import Tuple

from djitellopy import Tello


class UAV:
    def __init__(self):
        self.drone = Tello()
        self.drone.connect()
        print(f"UAV autonomies :  {self.drone.get_battery()}")

    def take_off(self):
        self.drone.takeoff()

    def forward(self, distance: int) -> None:
        self.drone.move_forward(distance)

    def left(self, deg: int) -> None:
        self.drone.move_left(deg)

    def right(self, deg: int) -> None:
        self.drone.move_right(deg)

    def get_frame(self):
        return self.drone.get_frame_read().frame

    def orientate(
        self, point: Tuple[int, int], width_picture: int, height_picture: int
    ) -> None:
        width, height = width_picture // 2, height_picture // 2
        diff_x = point[0] - width
        diff_y = point[1] - height

        if diff_x > 0:
            self.drone.rotate_clockwise(diff_x)
        elif diff_x < 0:
            self.drone.rotate_counter_clockwise(-diff_x)

        if diff_y > 0:
            self.drone.move_up(diff_y)
        elif diff_y < 0:
            self.drone.move_down(-diff_y)
