import cv2

from src.student import Student


def main():
    cap = cv2.VideoCapture(0)
    student_detector = Student()
    while True:
        _, img = cap.read()
        number_students = student_detector.search_number_total_students(img)
        cv2.putText(
            img,
            f"Number of students: {number_students}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        img = student_detector.draw_rectangle(img)

        cv2.imshow("frame", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
