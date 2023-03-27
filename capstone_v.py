# import libraries
import sqlite3
import os
#  ************************************* FUNCTION DEFINITIONS ******************************************

# ---------------------  CREATE OR CALL THE DATABASE
def caller():
    # create or open database 
    db = sqlite3.connect('./T39/ebookstore')
    # create cursor object
    cursor = db.cursor()
    # create table if it does not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS books(
        ID INT(255),
        TITLE VARCHAR(20),
        AUTHOR VARCHAR(20),
        QTY INT(255));''')
    # commit the changes into the db object
    db.commit()

    # call the cursor object again
    cursor = db.cursor()
    # create list of tuples (row) to insert and execute INSERT INTO... code
    data = [(3002,"Harry Potter and the Philosopher's Stone","J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
    (3004, "The Lord of the Rings","J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12)]
    
    # execute many
    cursor.executemany('''INSERT INTO books(ID,TITLE,AUTHOR,QTY) VALUES(?,?,?,?)''',
                        data)
    # commit the insert
    db.commit()
    # close the database
    db.close()

# ----------------------- 1) ENTERING A NEW BOOK IN THE DATABASE -------------------------

# define a function to generate an id for a new book
def id_setter():
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # select the last id 
    cursor.execute('''SELECT MAX(ID) FROM books''')
    max_id, = cursor.fetchone()
    return max_id + 1

# define a function that adds new data to the database
def appender(data):
    # connect to the database
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # INSERT the data
    cursor.execute('''INSERT INTO books(ID,TITLE,AUTHOR,QTY) VALUES(?,?,?,?)''',
                      data)
    # commit the changes to the database
    db.commit()
    # print out the new table
    cursor.execute('''SELECT * FROM books''')
    table = cursor.fetchall()
    print(table)

# Enter a new book
def enter():
    # ask information regarding the book
    title = input('Please enter the title of the book you would like to add to the database.\n')
    author = input('Please enter the name of the author of the book.\n')
    num = int(input('Please enter the quantity of this book you would like to add.\n'))
    # if the database does not yet exist, create it and then add the user input
    if not os.path.exists('./T39/ebookstore'):
        caller()
        id = id_setter()
        user_data = (id,title,author,num)
        appender(data = user_data)
        print('\n')
        print('The data entry has been successful!')
    # otherwise simply add the data to the database and print it
    else:
        print('File exists!\n')
        id = id_setter()
        user_data = (id,title,author,num)
        appender(data = user_data)
        print('\n')
        print('The data entry has been successful!')


#  -------------------- 2) UPDATING INFORMATION IN THE DATABASE ----------------------------

# Define a function that finds the identifier of the requested book
def identifier():
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # find info
    cursor.execute('''SELECT TITLE,ID FROM books''')
    book_tuple = cursor.fetchall()
    # manipulate the list of tuples to get a flattened list of books
    book_list = [{i[0]:i[1]} for i in book_tuple]
    book_options = [list(i.keys()) for i in book_list]
    book_final_list = [i[0] for i in book_options]
    # ask which book's information you want to update
    book = input(f'''Please choose and enter the book of your interest:\n{book_final_list}.\n''')

    # create a while else block to ensure the user entered names are valid
    while book not in book_final_list:
        print("This book is not in the system. Please try again.\n")
        book = input(f'''Please choose and enter which book's info you would like to amend 
from the available list below:\n{book_options}.\n''')
    else:
        # get id key of the book they want to update
        def returner(dictionary,name):
            for i in dictionary:
                if i.get(name) != None:
                    return i.get(name)
        # assign the id to a variable
        id_key = returner(dictionary = book_list,name = book)
        return id_key

def update_db():
    # connect to the database
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # use the identifier function to request the book name and get the id
    identity = identifier()
    # Create an exception object that will allow us to continue asking which field user wants to
    # update until they are completely done.
    not_complete = True
    while not_complete:
        # ask them which field they would like to update
        field = input("Which field would you like to update?. TITLE, AUTHOR OR QTY?\n").upper()
        while field not in ["TITLE","AUTHOR","QTY"]:
            print('You did not select a valid field.\n')
            field = input("Would you like to update the TITLE, AUTHOR OR QTY?\n").upper()

        else: # if the input is valid ask them what is the new info?
            if field == 'TITLE':
                title = input("What is the new title of this book?\n")
                cursor.execute('''UPDATE books SET TITLE = ? WHERE ID = ? ''',(title,identity))
                db.commit()
                cursor.execute('''SELECT * FROM books ''')
                table = cursor.fetchall()
                print(table)

            elif field == 'AUTHOR':
                author = input("Who is the new author of this book?\n")
                cursor.execute('''UPDATE books SET AUTHOR = ? WHERE ID = ? ''',(author,identity))
                db.commit()
                cursor.execute('''SELECT * FROM books ''')
                table = cursor.fetchall()
                print(table)

            else:
                num = int(input("What is the new quantity of this book?\n"))
                cursor.execute('''UPDATE books SET QTY = ? WHERE ID = ? ''',(num,identity))
                db.commit()
                cursor.execute('''SELECT * FROM books ''')
                table = cursor.fetchall()
                print(table)

            # ask them if they are finished editing or would like to continue?
            question = input("Would you like to continue updating other fields? Y or N \n")
            if question == 'N':
                    not_complete = False
    
    db.close()
#  ---------- Define a final updater function that checks if db exists yet or not.
def updater():
    if not os.path.exists('./T39/ebookstore'):
        caller()
        update_db()
        print('\n')
        print('The data update has been successful!')
    else:
        update_db()
        print('\n')
        print('The data update has been successful!')

#  ------------------- 3) DELETING INFORMATION FROM THE DATABASE ----------------------------------
def delete_db():
    # connect to the database
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # Add an exception object and while block to conditionally check if they want to delete multiple rows
    not_complete = True
    while not_complete:
        # use the identifier function to request the book name and get the id
        identity = identifier()
        cursor.execute('''DELETE FROM books WHERE ID = ? ''',(identity,))
        db.commit()
        cursor.execute('''SELECT * FROM books ''')
        table = cursor.fetchall()
        print(table)
        #ask if they are done
        question = input("Would you like to continue deleting? Y or N\n")
        if question == 'N':
            not_complete = False
    db.close()

# Final deletion function that checks if database exists already
def deleter():
    if not os.path.exists('./T39/ebookstore'):
        caller()
        delete_db()
        print('\n')
        print('The data deletion has been successful!')
    else:
        delete_db()
        print('\n')
        print('The data deletion has been successful!')



# ---------------------- 4) SEARCHING INFORMATION IN THE DATABASE ----------------------------------
# Task: search the database to find a specific book. To find book we can search by title, author or qty

def search_db():
    # connect to the database
    db = sqlite3.connect('./T39/ebookstore')
    # get a cursor object to run sql code
    cursor = db.cursor()
    # Add an exception object and while block to conditionally check if they want to delete multiple rows
    not_complete = True
    while not_complete:
        parameter = input("Would you like to search by TITLE,AUTHOR OR QTY?\n").upper()
        while parameter not in ['TITLE','AUTHOR','QTY']:
            print('You did not choose a valid option.\n')
            parameter = input("Would you like to search by TITLE,AUTHOR OR QTY?\n").upper()
        else:
            if parameter == 'TITLE':
                # use the identifier function to request the book name and get the id
                identity = identifier()
                cursor.execute('''SELECT * FROM books WHERE ID = ? ''',(identity,))
                row = cursor.fetchone()
                print(row)
            elif parameter == 'AUTHOR':
                    cursor.execute('''SELECT AUTHOR FROM books''')
                    author_tuple = cursor.fetchall()
                    author_list = [i[0] for i in author_tuple]
                    author = input(f"Please enter the name of the author of your interest from this list {author_list}.\n")
                    cursor.execute('''SELECT * FROM books WHERE AUTHOR = ? ''',(author,))
                    table = cursor.fetchall()
                    print(table)
            else:
                cursor.execute('''SELECT QTY FROM books''')
                qty_tuple = cursor.fetchall()
                qty_list = [i[0] for i in qty_tuple]
                exact_range = input("Would you like to search by an EXACT quantity or a RANGE from the available quantities?\n").upper()
                while exact_range not in ['EXACT','RANGE']:
                    exact_range = input("Would you like to search by an EXACT quantity or a RANGE?\n").upper()
                else:
                    if exact_range == 'EXACT':
                        qty = int(input(f"Please enter the quantity parameter from the following available quantities {qty_list}.\n"))
                        cursor.execute('''SELECT * FROM books WHERE QTY = ? ''',(qty,))
                        table = cursor.fetchall()
                        print(table)
                    else:
                        upper = int(input("Please enter the upper limit of the quantity parameter.\n"))
                        lower = int(input("Please enter the lower limit of the quantity parameter.\n"))
                        cursor.execute('''SELECT * FROM books WHERE QTY BETWEEN ? AND ?''',(lower,upper))
                        table = cursor.fetchall()
                        print(table)
        #ask if they are done
        question = input("Would you like to continue searching? Y or N\n")
        if question == 'N':
            not_complete = False
    db.close()

# Final search function that checks if database exists already
def searcher():
    if not os.path.exists('./T39/ebookstore'):
        caller()
        search_db()
        print('\n')
        print('Search successful!')
    else:
        search_db()
        print('\n')
        print('Search successful!')


# User interface function
def user_interface():
    not_complete = True
    while not_complete:
        print('Welcome to the ebookstore database. Please state which action you would like to complete today.\n')
        action = input('''Please type the number of the action you would like to perform:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit\n''')
        while action not in ['0','1','2','3','4']:
            print('You did not choose a valid action. Please try again.\n')
            action = input('''Please type the number of the action you would like to perform:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit\n''')
        else:
            if action == '1':
                enter()
            elif action == '2':
                updater()
            elif action == '3':
                deleter()
            elif action == '4':
                searcher()
            else:
                print('Goodbye!')
                break
        option = input("Would you like to continue with other actions?Y or N.\n").upper()
        if option == 'N':
            print('Goodbye!')
            not_complete = False


# *************************************** FUNCTION DEFINITIONS END **********************************


# RUN THE PROGRAM
user_interface()
