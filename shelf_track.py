# ========== Shelf Track System ==========
"""
This module functions as a bookstore inventory management system.

Users are able to add new books to the database, update book information,
delete books from the database and search the database for specific books
"""

# ========== Importing External Modules ==========
import sqlite3

from tabulate import tabulate

from contextlib import contextmanager


# ========== Database Functions ==========
@contextmanager
def db_connection(commit=False):
    """
    The context manager handles the SQLite database connections.

    This functions opens the connection to the "ebookstore.db" database.
    It then creates a cursor to assist in SQL operations, it also assists in
    commit and error handling.

    Parameters:
        commit (bool): If True, the changes that hapeen in the context block
                       is saved to the 'ebookstore.db' database.

    Yields:
        cursor(sqlite3.Cursor): Cursor object that carries our SQLite commands.
    """
    try:
        # Connect to the database.
        with sqlite3.connect('ebookstore.db') as conn:
            cursor = conn.cursor()

            # Make the cursor available to use in the context blocks.
            yield cursor

            # If commit is true, save the changes to the database.
            if commit:
                conn.commit()

    # Catch and print any database errors that occur.
    except sqlite3.Error as error:
        print(f"The following database error occurred: {error}")


def create_table():
    """
    This function will create the book table and author table in the
    'ebookstore.db', if they do not exist.

    Tables:
        - author(
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT
        )
        - book(
            id INTEGER PRIMARY KEY,
            title TEXT,
            authorID INTEGER,
            qty INTEGER
        )
    """
    try:
        # Open the database connection and commit changes.
        with db_connection(commit=True) as cursor:

            # Create the book table in the ebookstore database.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS book (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    authorID INTEGER NOT NULL,
                    qty INTEGER NOT NULL
                )
            ''')

            # Create the author table in the ebookstore database.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS author (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    country TEXT NOT NULL
                )
            ''')

    # Catch and print any database errors that occur.
    except sqlite3.Error as error:
        print(f"There was an error creating the table: {error}")


def data_sets():
    """
    This function will insert the book data into the book table and author
    data into the author table.
    """
    # Create a list of the book data.
    book_data = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)
    ]

    # Create a list of the author data.
    author_data = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K Rowling", "England"),
        (2356, "C.S Lewis", "Ireland"),
        (6380, "J.R.R Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")
    ]

    try:
        # Open the database connection and commit changes.
        with db_connection(commit=True) as cursor:

            # Insert or replace book_data in the book table.
            cursor.executemany('''
                INSERT OR REPLACE INTO book (id, title, authorID, qty)
                VALUES(? , ?, ?, ?)
            ''', book_data)

            # Insert or replace author_data in the author table.
            cursor.executemany('''
                INSERT OR REPLACE INTO author(id, name, country)
                VALUES(?, ?, ?)
            ''', author_data)

    # Catch and print any database errors that occur.
    except sqlite3.Error as error:
        print(f"There was an error inserting the data: {error}")


# ========== SYSTEM FUNCTIONS ==========


def menu():
    """
    Displays and loops the menu until the user selects a valid input or exits.

    When a valid input is selected, the respective function is called.
    """
    # Continuously request the user to enter an input until a valid
    # option is selected.
    while True:

        # Display the menu options.
        print(
            "\nMENU\n"
            "1. Enter book\n"
            "2. Update book\n"
            "3. Delete book\n"
            "4. Search books\n"
            "5. View details of all books\n"
            "0. Exit"
            )

        try:
            # Request the user to enter an input and convert to integer.
            menu_input = int(input(
                "Select one of the options from the menu above.\n"
                "Please enter the number only (0-5):\n"
                )
            )

        # Catch non-numeric inputs and print an error message.
        except ValueError:
            print("Invalid. Please enter a number from 0 - 5")
            continue

        # Check if the number is within the range.
        if menu_input < 0 or menu_input > 5:
            print("Invalid input. Please enter a number between 0 and 5")
            continue

        if menu_input == 1:
            enter_book()

        elif menu_input == 2:
            update_book()

        elif menu_input == 3:
            delete()

        elif menu_input == 4:
            search()

        elif menu_input == 5:
            view_details()

        elif menu_input == 0:
            print("Goodbye!")
            break


def enter_book():
    """
    This function allows the user to capture the details of a book, validates
    the inputs and then inserts the details into the database. If the author
    does not exist, the user is provided the option to add the author.
    """
    # ===== Validate book id =====

    # Continuously request the user to enter an input until the input is valid.
    while True:
        try:
            # Request the user to enter a book id and convert it to an integer.
            book_id = int(input("Please enter the book id:\n"))

            # Check if the input is a 4-digit number.
            if book_id < 1000 or book_id > 9999:
                print("Please enter a positive, 4 digit number")

                # If the input is invalid, continue to loop.
                continue
            break       # Exit the loop if the input it valid.

        except ValueError:
            # Print an error message if the input is not a number.
            print("Invalid input. Please enter a positive, 4 digit number.")

    # ===== Validate title =====

    # Continuously request the user to enter an input until the input is valid.
    while True:
        # Request the user to enter a title.
        title = input("Please enter the title of the book:\n").strip()

        # Check if the input is blank.
        if not title:
            print("The title cannot be blank.")

            # Continue to loop until the input is not blank.
            continue
        break       # Exit the loop if the input is not blank.

    # ===== Validate author ID =====

    # Continuously request the user to enter an input until the input is valid.
    while True:
        try:
            # Request the user to enter an author id and convert it to an
            # integer.
            author_id = int(input("Please enter the author ID:\n"))

            # Check if the input is a 4-digit number.
            if author_id < 1000 or author_id > 9999:
                print("The author id must be a positive, 4 digit number.")

                # If the input is invalid, continue to loop.
                continue
            break       # Exit the loop if the input it valid.

        except ValueError:
            # Print an error message if the input is not a number.
            print("Invalid input. Please enter a positive, 4 digit number.")

    try:
        # Open the database connection and create a cursor.
        with db_connection() as cursor:

            # Check if the author exists in the author table.
            cursor.execute('''
                SELECT id
                FROM author
                WHERE id = ?
            ''', (author_id,)
            )

            # Print message if the author does not exist.
            if cursor.fetchone() is None:
                print(f"The author ID {author_id} does not exist.\n")

                while True:
                    # Check if the user would like to add a new author.
                    new_auth = input(
                        "Would you like to add the author to the system? (y/n)"
                    ).strip().lower()

                    if new_auth == "y":
                        # Request the user to enter the author's name.
                        name = input(
                            "Please enter the author's name: \n"
                        ).strip()

                        # Check if the input is blank.
                        if not name:
                            print("This field cannot be blank.")
                            continue

                        # Check if the input starts with a letter.
                        if not name[0].isalpha():
                            print(
                                "The Author's name should start with a letter."
                            )
                            continue

                        # Check if the input is numeric.
                        if name.lstrip('-').isdigit():
                            print(
                                "The Author's name cannot consist of numbers."
                            )
                            continue

                        # Request the user to enter the author's country.
                        country = input(
                            "Please enter the author's country: \n"
                        ).strip()

                        # Check if the input is blank.
                        if not country:
                            print("This field cannot be blank.")
                            continue

                        # Check if the input starts with a letter.
                        if not country[0].isalpha():
                            print(
                                "The Author's name should start with a letter."
                            )
                            continue

                        # Check if the input is numeric.
                        if country.lstrip('-').isdigit():
                            print(
                                "The Author's name cannot consist of numbers."
                            )
                            continue

                        try:
                            # Insert the new author into the database.
                            with db_connection(commit=True) as cursor:
                                cursor.execute('''
                                    INSERT INTO author (id, name, country)
                                    VALUES(?, ?, ?)
                                ''', (author_id, name, country)
                                )

                                print("The author was added successfully.")
                                break       # Exit the create new author loop.

                        except sqlite3.Error as error:
                            print(f"Error inserting author: {error}")
                            return      # Exit function if db error occurs.

                    elif new_auth == "n":
                        # Exit function if user chooses not the add an author.
                        return

                    # Repeat the prompt if the input is incorrect.
                    else:
                        print("Please enter 'y' or 'n'")

    # Catch and print any database errors that occur.
    except sqlite3.Error as error:
        print(f"The following database error occurred: {error}")

    # ===== Validate quantity =====

    # Continuously request the user to enter an input until the input is valid.
    while True:
        try:
            # Request the user to enter a quantity and convert to an integer.
            qty = int(input("Please enter the quantity of books:\n"))

            # Check if the quantity is a negative number.
            if qty < 0:
                print("Quantity cannot be negative.")
                continue        # Continue to loop if the input is negative.

            break       # Exit the loop if the input is valid.

        except ValueError:
            # Print an error message if the input is a negative number.
            print("Invalid input. Please enter a positive number")

    # Try to insert the new book into the book table.
    try:
        with db_connection(commit=True) as cursor:
            # Insert the book into the database.
            cursor.execute('''
                INSERT INTO book (id, title, authorID, qty)
                VALUES(?, ?, ?, ?)
            ''', (book_id, title, author_id, qty))

            # Print success message.
            print(f"The book {title} has been added to the database")

    # Print error message if the book already exists.
    except sqlite3.IntegrityError:
        print(f"The book id {book_id} already exists in the database.")

    # Catch and print any database errors that occur.
    except sqlite3.Error as error:
        print(f"The following database error occurred: {error}")


def update_book():
    """
    This function validates the book ID entered by the user and then allows
    the user to update the quantity, title, author ID, author country and name.
    """
    try:
        with db_connection(commit=True) as cursor:
            # Fetch all books from the book table.
            cursor.execute('''
                SELECT * FROM book
            ''')

            book_list = cursor.fetchall()

    except sqlite3.Error as error:
        # Catch and print any database errors that occur.
        print(f"The following database error occurred: {error}")

    # Display a message if there are no books in the database.
    if not book_list:
        print("There are no books currently.")
        return

    # Display all books that are found, in a table format.
    print("\nCurrent Books:\n")
    headers = ["Book ID", "Title", "Author", "Quantity"]

    print(tabulate(book_list, headers=headers, tablefmt="fancy_grid"))

    # ===== Validate book ID =====

    # Continuously request the user to enter an input until the input is valid.
    while True:

        # Request the user to enter the book id.
        id_chosen = input(
            "\nPlease enter the ID of the book you would like to update: \n"
        )

        # Check if the input is numeric and has 4 digits.
        if not id_chosen.isdigit() or len(id_chosen) != 4:
            print("Invalid input. Please enter a positive 4 digit number")
            continue

        try:
            with db_connection() as cursor:
                # Fetch the book selected and the author information.
                cursor.execute('''
                    SELECT book.*, author.name, author.country
                    FROM book
                    INNER JOIN author
                    ON book.authorID = author.id
                    WHERE book.id = ?
                ''', (id_chosen,)
                )

                book_chosen = cursor.fetchone()

        except sqlite3.Error as error:
            # Catch and display errors that occur when retrieving the book.
            print(f"The following database error occurred: {error}")

            return      # Exit the function if a database error occurs.

        if book_chosen:
            break
        print("There was no book found with that ID. Please try again.")

    # Display the details of the selected book and the author, in a table
    # format.
    if book_chosen is not None:
        print("\nDetails of the chosen book:")

        details = [
            ["ID", book_chosen[0]],
            ["Title", book_chosen[1]],
            ["Author ID", book_chosen[2]],
            ["Quantity", book_chosen[3]],
            ["Author Name", book_chosen[4]],
            ["Author Country", book_chosen[5]],
        ]

        print(tabulate(details, tablefmt="fancy_grid"))

    # ===== Validate new quantity =====

    # Continuously request the user to enter an input until the input is valid.
    while True:
        try:

            # Request the user to enter a new quantity.
            update_qty = int(input("Please enter the new quantity:\n"))

            # Chceck that the input is not a negative number.
            if update_qty < 0:
                print("Please insert a positive number.")
                continue

            break       # Exit the loop if the input is valid.

        except ValueError:
            # Print error message for non-numeric inputs.
            print("Invalid input. Please enter a positive number.")

    try:
        with db_connection(commit=True) as cursor:
            # Update the details in the database.
            cursor.execute('''
                UPDATE book
                SET qty = ?
                WHERE id = ?
            ''', (update_qty, id_chosen))

    except sqlite3.Error as error:
        # Catch and display errors that occur during the update.
        print(f"The following database error occurred: {error}")
        return

    # Display success message.
    print("The quantity was successfully added.")

    # Ask the user if they would like to update the title, author or exit.
    while True:
        update_choice = input(
            "\nWould you like to update:\n"
            " [t] - The title\n"
            " [a] - The author id\n"
            " [an] - The author's name\n"
            " [ac] - The author's country\n"
            " [r] - Return to the main menu\n"
            "Enter your choice: "
        ).strip().lower()

        # ===== Title update =====
        if update_choice == "t":

            while True:

                # Request the user to enter the new title of the book.
                new_title = input(
                    "Please enter the new title of the book: \n"
                ).strip()

                # Check if input is blank
                if not new_title:
                    print("This field cannot be blank.")
                    continue        # Continue to loop if the input is blank.

                try:
                    with db_connection() as cursor:
                        # Check if the title of the book already exists:
                        cursor.execute('''
                            SELECT * FROM book
                            WHERE title = ? and id = ?
                        ''', (new_title, id_chosen)
                        )
                        title_match = cursor.fetchone()

                # Catch and display errors that occur during the title
                # validation.
                except sqlite3.Error as error:
                    print(f"The following database error occurred: {error}")

                # Display a message and continue to loop if title exists.
                if title_match:
                    print(
                        "The title already exists. Please enter a new title."
                    )
                    continue

                try:
                    with db_connection(commit=True) as cursor:
                        # Update the title in the database.
                        cursor.execute('''
                            UPDATE book
                            SET title = ?
                            WHERE ID = ?
                        ''', (new_title, id_chosen)
                        )

                # Catch and display errors that occur during the update
                # process.
                except sqlite3.Error as error:
                    print(f"The following database error occurred: {error}")

                # Display a success message to the user.
                print("The title was successfully updated.")
                break       # Exit the loop.

        # ===== Author ID update =====

        elif update_choice == "a":
            # Continue to loop until the user enters a valid input.
            while True:

                # Request the user to enter a new author ID.
                new_author_input = input("Please enter the new authorID: \n")

                try:
                    new_author_id = int(new_author_input)

                    # Check that the author id is positive and has 4 digits.
                    if not 1000 <= new_author_id <= 9999:
                        print("Please enter a positive 4 digit number.")

                    try:
                        with db_connection() as cursor:

                            # Check if the author exists in the author table.
                            cursor.execute('''
                                SELECT id
                                FROM author
                                WHERE id = ?
                            ''', (new_author_id,))

                            # Print message if the author does not exist.
                            if cursor.fetchone() is None:
                                print(
                                    f"The author ID {new_author_id} "
                                    "does not exist.\n"
                                )

                                while True:
                                    # Check if the user would like to add a
                                    # new author.
                                    new_auth = input(
                                        "Would you like to add the author to "
                                        "the system? (y/n)"
                                    ).strip().lower()

                                    if new_auth == "n":
                                        return

                                    elif new_auth == "y":
                                        # Request user to enter the author's
                                        # name.
                                        name = input(
                                            "Please enter the author's "
                                            "name: \n"
                                        ).strip()

                                        # Check if the input is blank.
                                        if not name:
                                            print(
                                                "This field cannot be blank."
                                            )
                                            continue

                                        # Check if the input starts with a
                                        # letter.
                                        if not name[0].isalpha():
                                            print(
                                                "The Author's name should "
                                                "start with a letter."
                                            )
                                            continue

                                        # Check if the input is numeric.
                                        if name.lstrip('-').isdigit():
                                            print(
                                                "The Author's name cannot "
                                                "consist of numbers."
                                            )
                                            continue

                                        # Request the user to enter the
                                        # author's country.
                                        country = input(
                                            "Please enter the author's "
                                            "country: \n"
                                        ).strip()
                                        # Check if the input is blank.
                                        if not country:
                                            print(
                                                "This field cannot be blank."
                                            )
                                            continue

                                        # Check if the input starts with a
                                        # letter.
                                        if not country[0].isalpha():
                                            print(
                                                "The Author's name should "
                                                "start with a letter."
                                            )
                                            continue

                                        # Check if the input is numeric.
                                        if country.lstrip('-').isdigit():
                                            print(
                                                "The Author's name cannot "
                                                "consist of numbers."
                                            )
                                            continue
                                        try:
                                            # Insert the new author into the
                                            # database.
                                            with db_connection(
                                                commit=True
                                            ) as cursor:

                                                cursor.execute(
                                                    '''
                                                    INSERT INTO author (
                                                        id,
                                                        name,
                                                        country
                                                    )
                                                    VALUES(?, ?, ?)
                                                    ''',
                                                    (
                                                        new_author_id,
                                                        name,
                                                        country
                                                    )
                                                )

                                                print(
                                                    "The autor was added "
                                                    "successfully."
                                                )

                                                # Exit the create new author
                                                # loop.
                                                break

                                        except sqlite3.Error as error:
                                            print("Error inserting author: "
                                                  f"{error}")

                                            # Exit function if db error occurs.
                                            return

                    except sqlite3.Error as error:
                        print(f"Error inserting author: {error}")

                    try:
                        with db_connection(commit=True) as cursor:

                            # Update the author id in the database
                            cursor.execute('''
                                UPDATE book
                                SET authorID = ?
                                WHERE id = ?
                            ''', (new_author_id, id_chosen)
                            )

                    # Catch and display errors that occur during the update.
                    except sqlite3.Error as error:
                        print(
                            f"The following database error occurred: {error}"
                        )

                    # Display success message and exit the loop.
                    print("The author ID has been successfully updated.")
                    break

                # Catch error and display message for non-numeric inputs.
                except ValueError:
                    print("Please enter a 4 digit numeric author ID.")

        # ===== Author name update =====

        # Continue to loop until the user enters a valid input.
        elif update_choice == "an":
            while True:
                # Request user to enter a new author name.
                new_auth_name = input(
                    "Please enter a new value for the Author's name: \n"
                ).strip()

                # Check if the input is blank.
                if not new_auth_name:
                    print("This field cannot be blank.")
                    continue

                # Check if the input starts with a letter.
                if not new_auth_name[0].isalpha():
                    print("The Author's name should start with a letter.")
                    continue

                # Check if the input is numeric.
                if new_auth_name.lstrip('-').isdigit():
                    print("The Author's name cannot consist of numbers.")
                    continue

                try:
                    with db_connection(commit=True) as cursor:
                        # Update the author's name in the database.
                        # book_chosen[2] is authorID
                        cursor.execute('''
                            UPDATE author
                            SET name = ?
                            WHERE id = ?
                        ''', (new_auth_name, book_chosen[2]))

                # Catch and display any errors that occur during the update.
                except sqlite3.Error as error:
                    print(f"The following database error occurred: {error}")

                # Display success message and exit the loop.
                print("The author's name has been updated successfully.")
                break

        # ===== Author country update =====

        elif update_choice == "ac":
            while True:
                # Request user to enter a new country
                new_country = input("Please enter a new country: \n").strip()

                # Check if the input is blank.
                if not new_country:
                    print("This field cannot be blank.")
                    continue

                # Check if the input starts with a letter
                if not new_country[0].isalpha():
                    print("The Country should start with a letter.")
                    continue

                # Check if the input is numeric.
                if new_country.lstrip('-').isdigit():
                    print("The country name cannot consist of numbers.")
                    continue

                try:
                    with db_connection(commit=True) as cursor:
                        # Update the country in the database.
                        cursor.execute('''
                            UPDATE author
                            SET country = ?
                            WHERE id = ?
                        ''', (new_country, book_chosen[2]))

                # Catch and display any database errors that occur during the
                # update.
                except sqlite3.Error as error:
                    print(f"The following database error occurred: {error}")

                # Print success message and exit the loop.
                print("The country has been successfully updated.")
                break

        # ===== Return to main menu =====
        elif update_choice == "r":
            break       # Exit the loop and return to main menu.

        # ===== Handle invalid inputs =====
        else:
            print("Please enter one of the options: 't', 'a', 'r' ")


def delete():
    """
    This function will allow the user to delete a book from the database.

    All the current books are displayed to the user. The user is then
    requested to enter the book id they wish to delete. The book ID is
    validated and then the book is deleted.
    """
    try:
        # Fetch all books from the book database.
        with db_connection() as cursor:
            cursor.execute('''
                SELECT * FROM book
            ''')
            book_list = cursor.fetchall()

    # Catch and display any database errors that occur during the
    # fetch.
    except sqlite3.Error as error:
        print(f"The following database error occurred: {error}")
        return

    # Check if the book list is empty and print a message.
    if not book_list:
        print("There are no current books to delete.")
        return

    # Display the book list in a table.
    print("\nBook List:\n")
    headers = ["Book ID", "Title", "Author", "Quantity"]

    print(tabulate(book_list, headers=headers, tablefmt="fancy_grid"))

    # Continuously request the user to enter an id until the input is valid.
    while True:
        id_input = input(
            "Please enter the ID of the book you would like to delete: \n"
        ).strip()

        try:
            id_selected = int(id_input)

            # Check that the book id is positive and has 4 digits.
            if not 1000 <= id_selected <= 9999:
                print("Please enter a positive 4 digit number.")
                continue

            try:
                with db_connection() as cursor:
                    # Check if the book is in the database.
                    cursor.execute('''
                        SELECT *
                        FROM book
                        WHERE id = ?
                    ''', (id_selected,)
                    )

                    book_found = cursor.fetchone()

                # If no book is found, display message and loop again.
                if not book_found:
                    print(f"The book with id {id_selected} was not found.")
                    continue

                # If the book exists, delete it from the database and exit
                # loop.
                with db_connection(commit=True) as cursor:
                    cursor.execute('''
                        DELETE FROM book
                        WHERE id = ?
                    ''', (id_selected,))

                    print(f"The book with id {id_selected} has been deleted.")
                    break

            # Catch and display any errors that occur during the deletion.
            except sqlite3.Error as error:
                print(f"The following database error occurred: {error}")
                return

        # Handle inputs that are not valid integers.
        except ValueError:
            print("Invalid input. Please enter a positive 4 digit number.")


def search():
    """
    This function allows the user to search for a book based on the book id.

    Request the user to enter a valid book ID. The function validates the
    input and then fetchs the book details.
    """
    # Continuously request the user to enter an id until the input is valid.
    while True:
        search_input = input(
            "Please enter the ID of the book you would like to search: \n"
        ).strip()

        # Check if the input is numeric by trying to convert it into an
        # integer.
        try:
            id_chosen = int(search_input)

            # Check that the book id is positive and has 4 digits.
            if not 1000 <= id_chosen <= 9999:
                print("Please enter a positive 4 digit number.")

            # Initialize the variable to None, to store the book if found.
            book_found = None

            try:
                with db_connection() as cursor:

                    # Search for the book in the book table.
                    cursor.execute('''
                        SELECT * FROM book
                        WHERE id = ?
                    ''', (id_chosen,))

                    # Fetch the first result.
                    book_found = cursor.fetchone()

                # Print book details, in a table.
                if book_found:
                    details = [
                        ["Book ID", book_found[0]],
                        ["Title", book_found[1]],
                        ["Author ID", book_found[2]],
                        ["Quantity", book_found[3]],
                    ]

                    print(tabulate(details, tablefmt="fancy_grid"))

                else:
                    # Display message if no books were found.
                    print(f"There are no books for id {id_chosen}")

                break

            # Catch and display any database errors that occur during the
            # search.
            except sqlite3.Error as error:
                print(f"The following database error occurred: {error}")

        # Handle non-numeric inputs.
        except ValueError:
            print("Invalid input. Please enter a positive 4 digit number.")


def view_details():
    """
    This function displays a list of the books, in the database, with their
    details.
    """
    try:
        with db_connection() as cursor:
            # Fetch the book titles, author names, and author countries
            # using an inner join.
            cursor.execute('''
                SELECT book.title, author.name, author.country
                FROM book
                INNER JOIN author
                ON book.authorID = author.id
            ''')
            book_details = cursor.fetchall()

    # Catch and display any database errors that occur during the
    # fetching process.
    except sqlite3.Error as error:
        print(f"The following database error occurred: {error}")
        return

    # Print the book details.
    print("\n Details")
    print("-" * 75)

    for title, name, country in book_details:
        print(f"Title: {title}\n")
        print(f"Author's Name: {name}\n")
        print(f"Author's Country: {country}")
        print("-" * 75)


# ========== System Function ==========

def run_system():
    """
    This function initializes and runs the functionality of the bookstore
    system.
    """
    try:
        # Create the tables, if they do not exist.
        create_table()

        # Populate the database with the data sets created.
        data_sets()

        # Call the main menu to allow th user to perform tasks.
        menu()

    # Catch and display any database errors that occur during the
    # set up process.
    except sqlite3.Error as error:
        print(f"The following database error has occurred: {error}")


# ========== Call Functions ==========

run_system()


# ========== References ==========
# https://www.programiz.com/sql/inner-join
# https://www.geeksforgeeks.org/python/re-match-in-python/
# https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
