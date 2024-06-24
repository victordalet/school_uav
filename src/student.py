from typing import List

import cv2


class Student:

    def __init__(self):
        self.number_total_students: int = 0
        self.number_student_by_class: List[int] = []
        self.students: List = []

    def search_number_total_students(self, frame: cv2.typing.MatLike) -> int:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        number_total_students = len(faces)
        self.number_total_students += number_total_students
        self.number_student_by_class.append(number_total_students)
        print(f"Number of students detected: {number_total_students}")
        return number_total_students

    def get_result_csv(self) -> None:
        with open('result.csv', 'w') as f:
            f.write('Total students\n')
            f.write(str(self.number_total_students) + '\n')
            f.write('Students by class\n')
            for i in self.number_student_by_class:
                f.write(str(i) + '\n')
