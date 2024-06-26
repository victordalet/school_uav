from typing import List

import cv2


class Student:
    def __init__(self):
        self.number_total_students: int = 0
        self.number_student_by_class: List[int] = []
        self.haar_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.students: List = []
        self.scale_factor: float = 1.1
        self.min_neighbors: int = 4

    def search_number_total_students(self, frame: cv2.typing.MatLike) -> int:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.haar_cascade.detectMultiScale(
            gray_frame, self.scale_factor, self.min_neighbors
        )
        number_total_students = len(faces)
        self.number_total_students += number_total_students
        self.number_student_by_class.append(number_total_students)
        print(f"Number of students detected: {number_total_students}")
        return number_total_students

    def draw_rectangle(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.haar_cascade.detectMultiScale(
            gray_frame, self.scale_factor, self.min_neighbors
        )
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame

    def get_result_csv(self) -> None:
        with open("result.csv", "w") as f:
            f.write("Total students\n")
            f.write(str(self.number_total_students) + "\n")
            f.write("Students by class\n")
            for i in self.number_student_by_class:
                f.write(str(i) + "\n")
