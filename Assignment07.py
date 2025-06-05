# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log:
#   HBrown, 5/31/2025, Created Script
# ------------------------------------------------------------------------------------------ #

import json

# -- Data -- #
# Define the data constants
MENU: str = """
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a student for a course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
"""
FILE_NAME: str = "Enrollments.json"

# Define the data variables
students: list = []     # a table of student data
menu_choice: str = ""   # holds the choice made by the user

class Person:
    """
    A class representing a person's data

    Properties:
    - first_name (str): the person's first name
    - last_name (str): the person's last name

    Change Log:
    HBrown, 5/31/2025, Created class
    """

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name


    @property
    def first_name(self):
        return self._first_name.title()
    @first_name.setter
    def first_name(self, name: str):
        if name.isalpha() or name == "":
            self._first_name = name
        else:
            raise ValueError("The first name cannot contain numbers!")


    @property
    def last_name(self):
        return self._last_name.title()
    @last_name.setter
    def last_name(self, name: str):
        if name.isalpha() or name == "":
            self._last_name = name
        else:
            raise ValueError("The last name cannot contain numbers!")


    def __str__(self):
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """
    A class representing a student's data

    Properties:
    - first_name (str): the student's first name
    - last_name (str): the student's last name
    - course_name (str): the name of the course the student is registering for

    Change Log:
    HBrown, 5/31/2025, Created class
    """

    def __init__(self, first_name: str = "",
                 last_name: str = "", course_name: str = ""):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name


    @property
    def course_name(self):
        return self._course_name.title()
    @course_name.setter
    def course_name(self, name: str):
        self._course_name = name


    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"


# -- Processing -- #
class FileProcessor:
    """
    A collection of processing layer functions that work with JSON files

    Change Log:
    RRoot, 1.1.2030, Created class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_objects: list):
        """ This function reads data from a JSON file and loads it into a list
        of dictionary rows then returns the list filled with student data.

        Change Log:
        RRoot, 1.1.2030, Created function
        HBrown, 6/3/2025 Modified function to convert dictionary data to Student object data

        :param file_name: string data with name of file to read from
        :param student_objects: list of dictionary rows to be filled with file data

        :return: list
        """

        try:
            # Get a list of dictionary rows from the data file
            file = open(file_name, 'r')
            json_students = json.load(file)

            # Convert the list of dictionary rows into a list of Student objects
            for student in json_students:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_objects.append(student_object)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages(
                message="Please make sure this file exists!",error=e)
        except Exception as e:
            IO.output_error_messages(
                message="Error: There was a problem with reading the file.",error=e)
        finally:
            if not file.closed:
                file.close()
        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from
        a list of dictionary rows

        Change Log:
        RRoot, 1.1.2030, Created function
        HBrown, 6/3/2025, Added code to convert Student objects to dictionary rows

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """

        try:
            student_data_dictionary: list = []
            for student in student_data:
                student_json: dict = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                student_data_dictionary.append(student_json)

            file = open(file_name, 'w')
            json.dump(student_data_dictionary, file, indent=2)
            file.close()
            print()
            print("Here is the data you just saved!:")
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if not file.closed:
                file.close()


# -- Presentation -- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    Change Log:
    RRoot, 1.1.2030, Created class
    RRoot, 1.2.2030, Added menu output and input functions
    RRoot, 1.3.2030, Added a function to display the data
    RRoot, 1.4.2030, Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays custom error messages to the user

        Change Log:
        RRoot, 1.3.2030, Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        Change Log:
        RRoot, 1.1.2030, Created function

        :return: None
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        Change Log:
        RRoot, 1.1.2030, Created function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        Change Log:
        RRoot, 1.1.2030, Created function
        HBrown, 6/3/2025, Modified code to access Student object data instead
        of dictionary data

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a
        course name from the user

        Change Log:
        RRoot, 1.1.2030, Created function

        :param student_data: list of dictionary rows to be filled with input data

        :return: list
        """

        try:
            student = Student()
            student.first_name = input("Enter the student's first name: ")
            student.last_name = input("Enter the student's last name: ")
            student.course_name = input("Please enter the name of the course: ")
            student_data.append(student)
            print()
            print(f"You have registered {student.first_name} "
                  f"{student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(
                message="One of the values was not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(
                message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(
    file_name=FILE_NAME, student_objects=students)

# Present and process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please choose option 1, 2, 3, or 4.")

print("Program Ended. Have a nice day!")