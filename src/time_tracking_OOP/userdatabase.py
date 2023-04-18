"""User database class"""

import sqlite3
import datetime
from time import strftime

class UserDatabase:
    """Class UserDatabase to store the user name and day information"""

    def __init__(self):
        pass

    def create_database(self):
        """Create the database"""
        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (name TEXT, day DATE, work_time DATE, break_time DATE)''')
            connection.commit()

    def add_user(self, name, day, work_time, break_time):
        """Add a new user to the database"""
        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            # in case user appears in the database, continue without adding the user again, no duplicates are created.
            try:
                cursor.execute('''INSERT INTO users (name, day, work_time, break_time) values(?,?,?,?)''',
                               (name, day, work_time, break_time))
                connection.commit()

            except:
                pass

    def find_user(self, name):
        """Check if a specific user is in the database"""

        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE name=?", (name,))
            # fetch the results and print them
            result = cursor.fetchone()

        if result:
            return result
        
    def clean_database(self):
        '''function to swipe clean database when wanted to'''

        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS users''')
            connection.commit()

    def see_database(self):
        '''function to print out entire database'''

        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            # fetch the results and print them
            result = cursor.fetchall()
            print(result)

    def add_work_time(self, work_time ,day, name):
        '''function to add total work time'''

        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE users set work_time=?, day=? WHERE name=?''',(work_time,day,name))
            connection.commit()

    def add_break_time(self, break_time, day, name):
        '''function to add total break time'''

        with sqlite3.connect('userdata.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''UPDATE users set break_time=?, day=? WHERE name=?''',(break_time,day,name))
            connection.commit()


#databaseObject = UserDatabase()
#databaseObject.create_database()       


# get player name + add player to database
#user_name = input("Enter user name: ")
#databaseObject.add_user(user_name, "18.04.2023", '00:00:00', '00:00:00')

# see what's inside database
#databaseObject.find_user(user_name)

# print out entire database
#databaseObject.see_database()

# clear entire database
#databaseObject.clean_database()

# create database again
#databaseObject.create_database()

# print out again entire database
#databaseObject.see_database()

