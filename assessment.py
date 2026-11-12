import json
import os
import math
from abc import ABC, abstractmethod


class Person(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def display_role(self):
        pass


class Student(Person):

    student_type = "Regular"

    def __init__(self, student_id, name, age, email, department, subject_marks):
        super().__init__(name)

        if not isinstance(student_id, int) or isinstance(student_id, bool) or student_id <= 0:
            raise ValueError("Invalid Student ID!")

        self.student_id = student_id
        self.age = age
        self.email = email
        self.department = department
        self.student_marks = subject_marks

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty!")
        self.__name = value.strip()

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("Invalid Age!")
        self.__age = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid Email!")

        value = value.strip()

        if value.count("@") != 1 or "." not in value.split("@")[-1] or " " in value:
            raise ValueError("Invalid Email!")

        self.__email = value

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Department cannot be empty!")
        self.__department = value.strip()

    @property
    def student_marks(self):
        return self.__student_marks

    @student_marks.setter
    def student_marks(self, value):

        if not isinstance(value, dict) or len(value) < 5:
            raise ValueError("Minimum 5 subjects required!")

        clean_marks = {}

        for subject, marks in value.items():

            if not isinstance(subject, str) or not subject.strip():
                raise ValueError("Invalid Subject Name!")

            if isinstance(marks, bool) or not isinstance(marks, (int, float)):
                raise ValueError("Marks must be numeric!")

            if not math.isfinite(marks) or not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100!")

            subject = subject.strip()

            if any(s.casefold() == subject.casefold() for s in clean_marks):
                raise ValueError("Duplicate Subject!")

            clean_marks[subject] = marks

        self.__student_marks = clean_marks

    def display_role(self):
        return "Regular Student"

    def calculate_total(self):
        return sum(self.student_marks.values())

    def calculate_average(self):
        return self.calculate_total() / len(self.student_marks)

    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        return "Fail"

    def check_status(self):
        return "Pass" if self.calculate_average() >= 60 else "Fail"

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "student_type": self.student_type,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "department": self.department,
            "student_marks": self.student_marks
        }


class MeritStudent(Student):

    student_type = "Merit"

    def display_role(self):
        return "Merit Student"

    def calculate_grade(self):

        if self.calculate_average() >= 85:
            return "A+"

        return super().calculate_grade()


class StudentManagement:

    def __init__(self):

        self.students = []
        self.next_id = 1
        self.filename = "students.json"

        self.load_students()

    def load_students(self):

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("Invalid student data format!")
                return

            for record in data:

                try:
                    student_id = record["student_id"]

                    if any(s.student_id == student_id for s in self.students):
                        continue

                    student_class = Student

                    if record.get("student_type") == "Merit":
                        student_class = MeritStudent

                    student = student_class(
                        student_id,
                        record["name"],
                        record["age"],
                        record["email"],
                        record["department"],
                        record["student_marks"]
                    )

                    self.students.append(student)

                    self.next_id = max(
                        self.next_id,
                        student.student_id + 1
                    )

                except (ValueError, KeyError, TypeError):
                    continue

        except FileNotFoundError:
            pass

        except (json.JSONDecodeError, OSError):
            print("Data file is corrupted or cannot be read!")

    def save_students(self):

        try:
            temporary_file = self.filename + ".tmp"

            with open(temporary_file, "w", encoding="utf-8") as file:

                json.dump(
                    [student.to_dict() for student in self.students],
                    file,
                    indent=4
                )

            os.replace(temporary_file, self.filename)
            return True

        except (OSError, TypeError, ValueError) as error:
            print("Error saving data:", error)
            return False

    def find_student(self, student_id):

        for student in self.students:

            if student.student_id == student_id:
                return student

        return None

    def show_menu(self):

        print("\n===== ADVANCED STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Class Statistics")
        print("7. Display Passed Students")
        print("8. Display Failed Students")
        print("9. Individual Result Report")
        print("10. Filter By Department")
        print("11. Filter By Grade")
        print("12. Sort By Name")
        print("13. Sort By Average")
        print("14. Display Top 3 Students")
        print("15. Exit")

    def add_student(self):

        name = input("Enter Full Name: ").strip()

        print("1. Regular Student")
        print("2. Merit Student")

        choice = input("Select Student Type: ")

        if choice == "1":
            student_class = Student
        elif choice == "2":
            student_class = MeritStudent
        else:
            print("Invalid Student Type!")
            return

        try:
            age = int(input("Enter Age: "))
            email = input("Enter Email: ")
            department = input("Enter Department: ")

            marks = {}

            for i in range(5):

                subject = input(f"Enter Subject {i+1}: ").strip()

                if not subject or any(s.casefold() == subject.casefold() for s in marks):
                    raise ValueError("Invalid or duplicate subject!")

                marks_value = float(input(f"Enter {subject} Marks: "))

                marks[subject] = marks_value

            student = student_class(
                self.next_id,
                name,
                age,
                email,
                department,
                marks
            )

            if self.find_student(student.student_id):
                raise ValueError("Duplicate Student ID!")

            self.students.append(student)
            self.next_id += 1

            if self.save_students():
                print("Student Added Successfully!")
                print("Student ID:", student.student_id)

        except ValueError as error:
            print("Invalid Input:", error)

    def display_one_student(self, student):

        print("\n-----------------------------")
        print("Student ID:", student.student_id)
        print("Student Type:", student.display_role())
        print("Name:", student.name)
        print("Age:", student.age)
        print("Email:", student.email)
        print("Department:", student.department)

        print("\nSubject Marks:")

        for subject, marks in student.student_marks.items():
            print(subject, ":", marks)

        print("Total:", student.calculate_total())
        print("Average:", round(student.calculate_average(), 2))
        print("Grade:", student.calculate_grade())
        print("Status:", student.check_status())

    def display_students(self):

        if not self.students:
            print("No Students Available!")
            return

        for student in self.students:
            self.display_one_student(student)

    def search_student(self):

        print("1. Search By ID")
        print("2. Search By Name")

        choice = input("Select Option: ")

        student = None

        if choice == "1":

            try:
                student_id = int(input("Enter Student ID: "))
                student = self.find_student(student_id)

            except ValueError:
                print("Invalid Student ID!")
                return

        elif choice == "2":

            name = input("Enter Full Name: ").strip()

            student = next(
                (s for s in self.students if s.name.casefold() == name.casefold()),
                None
            )

        else:
            print("Invalid Choice!")
            return

        if student:
            self.display_one_student(student)
        else:
            print("Student Not Found!")

    def update_student(self):

        try:
            student_id = int(input("Enter Student ID: "))

        except ValueError:
            print("Invalid Student ID!")
            return

        student = self.find_student(student_id)

        if student is None:
            print("Student Not Found!")
            return

        print("1. Update Name")
        print("2. Update Age")
        print("3. Update Email")
        print("4. Update Department")
        print("5. Update Subject Marks")

        choice = input("Select Option: ")

        try:

            if choice == "1":
                student.name = input("Enter New Name: ")

            elif choice == "2":
                student.age = int(input("Enter New Age: "))

            elif choice == "3":
                student.email = input("Enter New Email: ")

            elif choice == "4":
                student.department = input("Enter New Department: ")

            elif choice == "5":

                subject = input("Enter Subject Name: ").strip()

                existing = next(
                    (s for s in student.student_marks
                     if s.casefold() == subject.casefold()),
                    None
                )

                if existing is None:
                    print("Subject Not Found!")
                    return

                marks = float(input("Enter New Marks: "))

                updated_marks = student.student_marks.copy()
                updated_marks[existing] = marks

                student.student_marks = updated_marks

            else:
                print("Invalid Choice!")
                return

            self.save_students()
            print("Student Updated Successfully!")

        except ValueError as error:
            print("Invalid Input:", error)

    def delete_student(self):

        try:
            student_id = int(input("Enter Student ID: "))

        except ValueError:
            print("Invalid Student ID!")
            return

        student = self.find_student(student_id)

        if student is None:
            print("Student Not Found!")
            return

        self.display_one_student(student)

        confirmation = input("Delete Student? (yes/no): ").strip().lower()

        if confirmation == "yes":

            self.students.remove(student)
            self.save_students()

            print("Student Deleted Successfully!")

        elif confirmation == "no":
            print("Deletion Cancelled!")

        else:
            print("Invalid Confirmation!")

    def class_statistics(self):

        if not self.students:
            print("No Students Available!")
            return

        total = len(self.students)

        passed = [s for s in self.students if s.check_status() == "Pass"]
        failed = [s for s in self.students if s.check_status() == "Fail"]

        highest = max(self.students, key=lambda s: s.calculate_average())
        lowest = min(self.students, key=lambda s: s.calculate_average())

        overall_average = sum(
            s.calculate_average() for s in self.students
        ) / total

        grade_count = {
            "A+": 0,
            "A": 0,
            "B": 0,
            "C": 0,
            "Fail": 0
        }

        department_count = {}

        for student in self.students:

            grade = student.calculate_grade()
            grade_count[grade] += 1

            department = student.department

            department_count[department] = department_count.get(department, 0) + 1

        print("\n===== CLASS STATISTICS =====")

        print("Total Students:", total)
        print("Passed Students:", len(passed))
        print("Failed Students:", len(failed))
        print("Overall Average:", round(overall_average, 2))

        print("\nHighest Student:", highest.name)
        print("Highest Average:", round(highest.calculate_average(), 2))

        print("\nLowest Student:", lowest.name)
        print("Lowest Average:", round(lowest.calculate_average(), 2))

        print("\nGrade Wise Count:")

        for grade, count in grade_count.items():
            print(grade, ":", count)

        print("\nDepartment Wise Count:")

        for department, count in department_count.items():
            print(department, ":", count)

    def display_by_status(self, status):

        matching = [
            s for s in self.students
            if s.check_status() == status
        ]

        if not matching:
            print("No Matching Students!")
            return

        for student in matching:
            self.display_one_student(student)

    def student_report(self):

        try:
            student_id = int(input("Enter Student ID: "))

        except ValueError:
            print("Invalid Student ID!")
            return

        student = self.find_student(student_id)

        if student is None:
            print("Student Not Found!")
            return

        print("\n===== INDIVIDUAL RESULT REPORT =====")

        self.display_one_student(student)

        print("Maximum Marks:", len(student.student_marks) * 100)

    def filter_by_department(self):

        department = input("Enter Department: ").strip()

        matching = [
            s for s in self.students
            if s.department.casefold() == department.casefold()
        ]

        self.display_matching(matching)

    def filter_by_grade(self):

        grade = input("Enter Grade: ").strip().upper()

        if grade not in ["A+", "A", "B", "C", "FAIL"]:
            print("Invalid Grade!")
            return

        matching = [
            s for s in self.students
            if s.calculate_grade().upper() == grade
        ]

        self.display_matching(matching)

    def display_matching(self, students):

        if not students:
            print("No Matching Students!")
            return

        for student in students:
            self.display_one_student(student)

    def sort_by_name(self):

        sorted_students = sorted(
            self.students,
            key=lambda s: s.name.casefold()
        )

        self.display_matching(sorted_students)

    def sort_by_average(self):

        sorted_students = sorted(
            self.students,
            key=lambda s: s.calculate_average(),
            reverse=True
        )

        self.display_matching(sorted_students)

    def display_top_three(self):

        top_students = sorted(
            self.students,
            key=lambda s: s.calculate_average(),
            reverse=True
        )[:3]

        if not top_students:
            print("No Students Available!")
            return

        print("\n===== TOP 3 STUDENTS =====")

        for position, student in enumerate(top_students, start=1):

            print("\nPosition:", position)
            print("Name:", student.name)
            print("Average:", round(student.calculate_average(), 2))
            print("Grade:", student.calculate_grade())

    def run(self):

        while True:

            self.show_menu()

            choice = input("Enter Your Choice: ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.display_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                self.class_statistics()

            elif choice == "7":
                self.display_by_status("Pass")

            elif choice == "8":
                self.display_by_status("Fail")

            elif choice == "9":
                self.student_report()

            elif choice == "10":
                self.filter_by_department()

            elif choice == "11":
                self.filter_by_grade()

            elif choice == "12":
                self.sort_by_name()

            elif choice == "13":
                self.sort_by_average()

            elif choice == "14":
                self.display_top_three()

            elif choice == "15":
                print("Thank You For Using Student Management System!")
                break

            else:
                print("Invalid Choice! Please Try Again!")


if __name__ == "__main__":
    app = StudentManagement()
    app.run()
