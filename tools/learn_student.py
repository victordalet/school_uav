import sys

import cv2

from src.student import Student


def main():
    student_detector = Student()
    student_detector.learn()
    random_picture = sys.argv[1]
    student_detector.recognize(cv2.imread(random_picture))


if __name__ == "__main__":
    main()
