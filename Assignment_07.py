#---------------------------------------------------------------------------------- #
#Title: Assignment07
#Desc: Classes and Objects
#Change Log: (Who, When, What)
#Disha, 9/10/2024,Created Script
#---------------------------------------------------------------------------------- #
import json
from itertools import filterfalse
from json import JSONDecodeError
from typing import TextIO, IO

MENU: str='''\n--- Course Registration Program ---
Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------'''

FILE_NAME: str = "Enrollments.json"

# Extract the data from the file.

class person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property  # (Use this decorator for the getter or accessor)
    def first_name(self) -> str:
        return self._first_name.title()  # Optional formatting code

    @first_name.setter
    def first_name(self, value: str) -> None:
        if value.isalpha() or value == "":  # allow characters or the default empty string
            self._first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self) -> str:
        return self._last_name.title()  # Optional formatting code

    @last_name.setter
    def last_name(self, value: str) -> None:
        if value.isalpha() or value == "":  # allow characters or the default empty string
            self._last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self) -> str:
        return f'{self.first_name},{self.last_name}'

class student(person):

    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self._course_name.title()  # Optional formatting code

    @course_name.setter
    def course_name(self, value: str):
        self._course_name = value

    def __str__(self) -> str:
        return f'{self.first_name},{self.last_name},{self.course_name}'

class FileProcessor:

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list[student]) -> list[student]:
        '''
        This function reads the data from a json file and returns a list of dictionaries.
        :param file_name: string, the name of the file to read.
        :return: The student table which is of type list.
        '''
        file_data = []
        file = None
        try:
            file = open(file_name, "r")
            file_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages(message="Error: There was an error reading the file", error=e)
            IO.output_error_messages(message="Creating file since it doesn't exist.", error=e)

        finally:
            if file is not None and not file.closed:
                file.close()
        for row in file_data:
            student_data: list[student] = []
            student_data.append(
                student(row['first_name'], row['last_name'], row['course_name'])
            )
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[student]):
        """ This function writes data to a json file with data from a list of dictionary rows"""
        file_data=[]
        for student in student_data:
            file_data.append({"first_name": student.first_name,
                              "last_name": student.last_name,
                              "course_name": student.course_name})
        file=None
        try:
            file = open(file_name, "w")
            json.dump(file_data, file)
            file.close()
            IO.output_student_courses(student_data=student_data)
        except TypeError as e:
            IO.output_error_messages(message="There was an error writing the file", error=e)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file is not None and not file.closed:
                file.close()

class IO:
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("--Technical Error Message--")
            print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def output_menu(menu: str):
        ''' This function displays the menu of choices to the user
        '''
        print() # Adding extra space to make it look nicer.
        print(menu)
        print() # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ['1', '2', '3','4']:
                raise Exception("Please, choose only 1,2,3 or 4")
        except Exception as e:
            IO.output_error_messages(e. __str__())

        return choice

    @staticmethod
    def output_student_courses(student_data: list[student]):
        ''' This function displays the student and course name to the user.
        '''
        print("_" * 50)
        for student in student_data:
            print(f'student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("_" * 50)

    @staticmethod
    def input_student_data(student_data: list[student])-> list[student]:
        ''' This function gets the student's first name and last name, with a course name from the user.
        :return: list'''

        try:
            # Input the data:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            students = student(student_first_name,
                              student_last_name,
                              course_name)
            student_data.append(students)
            print()
            print(f"You have registered {student_first_name},{student_last_name} for {course_name}\n")
        except ValueError as e:
            IO.output_error_messages(message='Invalid input', error=e)
        except Exception as e:
            IO.output_error_messages(message='There was a problem with your entered data.', error=e)
        return student_data

# Define the data Variables:
students: list[student] = [] # a table of student data.
menu_choice: str # Holds the choice made by the user.

# When the program starts, read the file data into a list of lists (table)
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and process the data.
while True:

    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data:
    if menu_choice == '1':  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data:
    elif menu_choice == '2': # Process the data to create and display a custom message.
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file.
    elif menu_choice == '3':
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop:
    elif menu_choice == '4':
        break
    else:
        print("You made invalid choice. Please try again. ")

print("Program Ended")

