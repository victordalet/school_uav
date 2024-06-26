import os
from typing import List
import face_recognition
from tqdm import tqdm
import cv2


class Student:
    directories: List[str]
    faces_encodings: List[List]
    student_name_by_class: List[List[str]]

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

    def get_result_csv_recognize(self) -> None:
        with open("result.csv", "w") as f:
            f.write("Total students\n")
            f.write(str(self.number_total_students) + "\n")
            f.write("Students by class\n")
            for i in self.number_student_by_class:
                f.write(str(i) + "\n")
            f.write("Students\n")
            for i in self.students:
                f.write(str(i) + "\n")

    def learn(self) -> None:
        self.directories = os.listdir("classes")
        self.faces_encodings = []
        index_classes = 0
        for directory in self.directories:
            self.student_name_by_class.append([])
            self.faces_encodings.append([])
            for file in tqdm(os.listdir(f"classes/{directory}")):
                self.student_name_by_class[index_classes].append(file.split(".")[0])
                image = face_recognition.load_image_file(f"classes/{directory}/{file}")
                face_encoding = face_recognition.face_encodings(image)[0]
                self.faces_encodings[index_classes].append(face_encoding)
            index_classes += 1

    def recognize(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.haar_cascade.detectMultiScale(
            gray_frame, self.scale_factor, self.min_neighbors
        )
        for x, y, w, h in faces:
            face = frame[y : y + h, x : x + w]
            face_encoding = face_recognition.face_encodings(face)
            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]
                for index_classes in range(len(self.faces_encodings)):
                    results = face_recognition.compare_faces(
                        self.faces_encodings[index_classes], face_encoding
                    )
                    for i, result in enumerate(results):
                        if result:
                            cv2.putText(
                                frame,
                                self.student_name_by_class[index_classes][i],
                                (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (255, 255, 255),
                                2,
                                cv2.LINE_AA,
                            )
                            self.students.append(
                                self.student_name_by_class[index_classes][i]
                            )
                            self.number_student_by_class[index_classes] += 1
                            self.number_total_students += 1

        return frame
