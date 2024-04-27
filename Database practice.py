import sqlite3


def main():
    # Connect to the phonebook database. Create the database if it does not already exist.
    sql_conn = sqlite3.connect('phonebook.db')

    # Create a cursor to read through the database.
    cursor = sql_conn.cursor()

    # Create a new table called "Entries" if there is not already an Entries table in the database.
    new_table = '''CREATE TABLE IF NOT EXISTS Entries (
                        EntriesID INTEGER PRIMARY KEY NOT NULL, 
                        FirstName TEXT, 
                        LastName TEXT, 
                        PhoneNumber TEXT NOT NULL, 
                        IsActive INTEGER NOT NULL)'''
    
    # Use the cursor to create the new table using the new_table query.
    cursor.execute(new_table)

    # Call the menu() method
    menu(sql_conn, cursor)

# End of main() method


# Menu method
def menu(sql_conn, cursor):
    print('Menu')
    print('1: Add a New Record')
    print('2: Look Up a Phone Number')
    print('3: Update a Phone Number')
    print('4: Delete a Record')
    print('5: Quit')
    print('--------------------\n')
    
    user_input = int(input('Enter the number of the menu option you would like to select: '))

    # Verify that the user entered a number between 1 and 5
    if 0 < user_input < 6:

            # Calls add method
            if user_input == 1:
                add_number(cursor)
                menu(sql_conn, cursor)

            # Calls lookup method
            elif user_input == 2:
                lookup_number(cursor)
                menu(sql_conn, cursor)

            # Calls edit method
            elif user_input == 3:
                edit_number(cursor)
                menu(sql_conn, cursor)

            # Calls delete method
            elif user_input == 4:
                delete_number(cursor)
                menu(sql_conn, cursor)
            
            # This section will commit any changes, close the database connection, and end the program.
            elif user_input == 5:
                sql_conn.commit()
                sql_conn.close()
                print('Thank you for using the Phone Number program.\n')

    # Error handling
    else:
        print('That was not a valid selection.\n')
        menu(sql_conn, cursor)

# Method to add a new record with name and phone number.
def add_number(cursor):
    # Boolean variables to check input validity
    is_first_name_valid = False
    is_last_name_valid = False
    is_phone_num_valid = False

    # Use isalpha() to get the correct type of input for names
    if not is_first_name_valid:
        print('\n')
        first_name = input('Enter the first name: ')

        if not first_name.isalpha():
            print('\n')
            print('That name is not valid.\n')
            first_name = input('Enter the first name: ')
            print('\n')
        else:
            is_first_name_valid = True

    # Use isalpha() to get the correct type of input for names
    if not is_last_name_valid:
        print('\n')
        last_name = input('Enter the last name: ')

        if not last_name.isalpha():
            print('\n')
            print('That name is not valid.')
            first_name = input('Enter the last name: ')
            print('\n')
        else:
            is_last_name_valid = True

    # Use isnumeric() to get the correct type of input for phone number
    if not is_phone_num_valid:
        phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')

        if not phone_num.isnumeric():
            print('\n')
            print('That phone number is not valid.\n')
            phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')
            print('\n')
        else:
            is_phone_num_valid = True

    # If all variables were entered correctly, add the new record to the Entries table.
    if is_first_name_valid and is_last_name_valid and is_phone_num_valid:
        cursor.execute('''INSERT INTO Entries (FirstName, LastName, PhoneNumber, IsActive)
                          VALUES (?, ?, ?, ?)''', 
                         (first_name, last_name, phone_num, 1))
        
        # Notify the user that the new record was added.
        print('Record was added successfully.\n')
        
    # Return to the menu if something went wrong with adding a record.
    else:
        print('The new record was not added. Returning to the menu.\n')

# Method to look up a record using the phonen number
def lookup_number(cursor):
        print('What is the phone number you would like to look up?')
        phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')

        cursor.execute('''SELECT FirstName, LastName, PhoneNumber from Entries where
                          PhoneNumber == ? and IsActive == 1''', (phone_num,))
        record = cursor.fetchone()

        if record != None:
            print('\n')
            print(record)
            print('\n')
        else:
            print('Phone number was not found.\n')


# This method allows the user to update a phone number in the database. 
# I am not currently concerned about updating names in the database records.
def edit_number(cursor):
    
    # Get the existing phone number from the user.
    print('\n')
    print('What is the phone number you would like to change?\n')
    phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')

    # Find the database record that contains the existing phone number.
    cursor.execute('''SELECT PhoneNumber from Entries where 
                      PhoneNumber == ? and IsActive == 1''', (phone_num,))
    record = cursor.fetchone()

    # If the phone number exists in the database, get the new number from the user.
    if record != None:
        print('\n')
        print('What is the new phone number?\n')
        new_phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')

        # Replace the existing phone number with the new number.
        cursor.execute('''UPDATE Entries set PhoneNumber = ? where PhoneNumber == ?''',
                        (new_phone_num, phone_num,))
        
        # Get the record with the new phone number
        cursor.execute('''SELECT FirstName, LastName, PhoneNumber from Entries where
                          PhoneNumber == ? and IsActive == 1''', (new_phone_num,))
        record = cursor.fetchone()

        # Print the record with the new phone number if it exists
        if record != None:
            print('\n')
            print(record)
            print('\n')
        else:
            print('That phone number could not be found. Please try again.\n')
    
    # If the phone number did not exist in the database, notify the user.
    else:
        print('That phone number could not be found. Please try again.\n')

# This method allows the user to do a logical delete on a record from the database.
def delete_number(cursor):
    # Get the existing phone number from the user.
    print('\n')
    print('What is the phone number you would like to delete?\n')
    phone_num = input('Enter the phone number WITHOUT spaces, dashes, or parentheses: ')

    # Do a logical delete of the record by changing the IsActive column from 1 to 0 for this record.
    # This is how records are deleted where I work.
    # We do this so we can view the table history and so the Primary Key / table ID column can remain sequential.
    # Fully deleting a table row will cause the table ID to skip numbers. Example: 1 2 3 4 5 becomes 1 3 4.
    cursor.execute('''UPDATE Entries set IsActive = 0 where 
                      PhoneNumber == ?''', (phone_num,))

    # Verify that the logical delete was successful by searching for the phone number and an active record.
    # This should result in an empty record variable.
    cursor.execute('''SELECT PhoneNumber from Entries where 
                      PhoneNumber == ? and IsActive == 1''', (phone_num,))
    record = cursor.fetchone()
    
    if record != None:
        print('\n')
        print('Something went wrong. Returing to the menu.\n')
    else:
        print('\n')
        print('Record was deleted successfully.\n')


# Call main()
if __name__ == '__main__':
    main()
