import mysql.connector as sqltor
from datetime import date, datetime, timedelta
import os

DB_NAME = 'library'

##############################################
# Methods to initialize tables and databases #
##############################################
TABLES = {}
TABLES['students'] = (
    "CREATE TABLE `students` ("
    "  `student_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  `class` varchar(30) NOT NULL,"
    "  `roll_no` int(11) NOT NULL,"
    "  `section` varchar(10) NOT NULL,"
    "  PRIMARY KEY (`student_id`)"
    ") ENGINE=InnoDB;")


TABLES['books'] = (
    "CREATE TABLE `books` ("
    "  `book_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  `author` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`book_id`)"
    ") ENGINE=InnoDB")

TABLES['bookings'] = (
    "CREATE TABLE `bookings` ("
    "  `booking_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `student_id` int(11) NOT NULL,"
    "  `book_id` int(11) NOT NULL,"
    "  `issue_date` date NOT NULL,"
    "  `return_date` date,"
    "  PRIMARY KEY (`booking_id`)"
    ") ENGINE=InnoDB")

#############################
# Method to create entities #
#############################

def create_database(cursor):
    try:
        cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except sqltor.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

##########################
# Method to use database #
##########################

def use_database(cursor):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except sqltor.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == sqltor.errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cursor.execute("USE {}".format(DB_NAME))
        else:
            print(err)
            exit(1)

#######################
# Method to add table #
#######################
def add_tables(cursor, tables):
    for table_name in tables:
        table_description = tables[table_name]
        try:
            cursor.execute(table_description)
        except sqltor.Error as err:
            None
        else:
	        print("OK")

###########################
# Methods to add entities #
###########################

def add_students(cursor, name, roll_no, standard, section):
    add_student = ("INSERT INTO students "
               "(name, class, roll_no, section) "
               "VALUES (%s, %s, %s, %s)")
    data_student = (name, roll_no, standard, section)
    cursor.execute(add_student, data_student)
    database_connection.commit();

def add_books(cursor, name, author):
    add_book = ("INSERT INTO books "
        "(name, author)"
        "VALUES (%s, %s)")
    data_book = (name, author)
    cursor.execute(add_book, data_book)
    database_connection.commit();


def add_bookings(cursor, book_id, student_id, issue_date):
    add_booking = ("INSERT INTO bookings "
        "(book_id, student_id, issue_date) "
        "VALUES (%s, %s, %s)")
    data_booking = (book_id, student_id, issue_date)
    cursor.execute(add_booking, data_booking)
    database_connection.commit();

################################
# Methods to show all entities #
################################

def show_books(cursor):
    show_students = ("select * from books;")
    cursor.execute(show_students)
    for book in cursor:
        #curly brackets are for appending information
        print("Book ID: {}, Name: {}, Author: {}".format(book[0], book[1], book[2])) 

def show_students(cursor):
    show_students = ("select * from students;")
    cursor.execute(show_students)
    for student in cursor:
        print("Student ID: {}, Name: {}, Roll No: {}, Class: {}, Section: {}".format(student[0], student[1], student[2], student[3], student[4]))

def show_bookings(cursor):
    show_booking = ("select bookings.booking_id," 
        "students.student_id, students.name," 
        "students.roll_no, books.book_id," 
        "books.name, issue_date, return_date from bookings " 
        "join students on students.student_id = bookings.student_id " 
        "join books on books.book_id = bookings.book_id;")

    cursor.execute(show_booking)
    for booking in cursor:
        print("Booking Id: {}, Book Id: {}, Book Name: {}, Student Name: {}, Roll No: {}, Issue Date: {}, Return Date: {}".format(booking[0], booking[4], booking[5], booking[2], booking[3], booking[6], booking[7]))

###########################
# Method to find entities #
###########################

def find_book(cursor, book_name):
    show_students = ("select * from books where name like \"{}%\";".format(book_name))
    cursor.execute(show_students)
    for book in cursor:
        print("Book ID: {}, Name: {}, Author: {}".format(book[0], book[1], book[2])) 

def find_student(cursor, student_id):
    show_students = ("select * from students where student_id = {};".format(student_id))
    cursor.execute(show_students, student_id)
    for student in cursor:
        print("Student ID: {}, Name: {}, Roll No: {}, Class: {}, Section: {}".format(student[0], student[1], student[2], student[3], student[4]))

def find_booking(cursor, booking_id):
    show_booking = ("select bookings.booking_id," 
        "students.student_id, students.name," 
        "students.roll_no, books.book_id," 
        "books.name, issue_date, return_date from bookings " 
        "join students on students.student_id = bookings.student_id " 
        "join books on books.book_id = bookings.book_id where booking_id = {};".format(booking_id))

    cursor.execute(show_booking, booking_id)
    for booking in cursor:
        print("Booking Id: {}, Book Id: {}, Book Name: {}, Student Name: {}, Roll No: {}, Issue Date: {}, Return Date: {}".format(booking[0], booking[4], booking[5], booking[2], booking[3], booking[6], booking[7]))

##############################
# Methods to update entities #
##############################
def update_booking(cursor, booking_id, return_date):
    show_students = "update bookings set return_date = \"{}\" where booking_id = {};".format(return_date.strftime("%Y-%m-%d"), booking_id)
    cursor.execute(show_students)
    database_connection.commit()

##############################
# Methods to manage entities #
##############################

def manage_books(cursor):
    while(True):
        os.system('clear')
        print("What do you want to do?")
        print("1. See all books.")
        print("2. Search book")
        print("3. Add a new book")
        print("4. Back")
        option = int(input("Please enter your choice: "))

        if int(option) not in range(1, 6): 
            print("Please choose correct option")
            continue
        elif option == 4:
            break
        elif option == 1:
            show_books(cursor)
        elif option == 2:
            book_id = input("Please enter book name: ")
            find_book(cursor, book_id)
        elif option == 3:
            book_name = input("Please enter book name: ")
            author = input("Please enter author name: ")
            add_books(cursor, book_name, author)
            print("Book has been addded!!!!")
        

        input("Press key to continue...")

def manage_students(cursor):
    while(True):
        os.system('clear')
        print("What do you want to do?")
        print("1. See all students.")
        print("2. Search student")
        print("3. Add new student")
        print("4. Back")
        option = int(input("Please enter your choice: "))

        if int(option) not in range(1, 6): 
            print("Please choose correct option")
            continue
        elif option == 4:
            break
        elif option == 1:
            show_students(cursor)
        elif option == 2:
            student_id = int(input("Please enter student id: "))
            find_student(cursor, student_id)
        elif option == 3:
            name = input("Please enter student name: ")
            roll_no = input("Please enter roll no: ")
            standard = input("Please enter class: ")
            section = input("Please enter section: ")
            add_students(cursor, name, roll_no, standard, section)
            print("Student has been addded!!!!")
        

        input("Press key to continue...")

def manage_bookings(cursor):
    while(True):
        os.system('clear')
        print("What do you want to do?")
        print("1. See all booking")
        print("2. See student bookings")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Back")
        option = int(input("Please enter your choice: "))

        if int(option) not in range(1, 6): 
            print("Please choose correct option")
            continue
        elif option == 5:
            break
        elif option == 1:
            show_bookings(cursor)
        elif option == 2:
            booking_id = int(input("Please enter booking id: "))
            find_booking(cursor, booking_id)
        elif option == 3:
            student_id = input("Please enter student id: ")
            book_id = input("Please enter book_id id: ")
            add_bookings(cursor, book_id, student_id, date.today())
            print("Student has been added!!!!")
        elif option == 4: 
            booking_id = int(input("Please enter booking id: "))
            update_booking(cursor, booking_id, date.today())
            print("Book returned!!!!!!!!")
        input("Press key to continue...")

############################
# Method to manage Program #
############################

if __name__ == "__main__":
    database_connection = sqltor.connect(host="localhost", user="root", passwd="")
    cursor = database_connection.cursor()
    use_database(cursor)
    add_tables(cursor, TABLES)

    while(True):
        os.system('clear')
        print("Welcome to library")
        print("What do you want to do?")
        print("1. Manage books.")
        print("2. Manage students.")
        print("3. Manage bookings.")
        print("4. Quit")
        option = int(input("Please enter your choice: "))

        if int(option) not in range(1, 5): 
            print("Please choose correct option")
            continue
        elif option == 4:
            break
        elif option == 1:
            manage_books(cursor)            
        elif option == 2:
            manage_students(cursor)
        elif option == 3:
            manage_bookings(cursor)
