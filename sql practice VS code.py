import sqlite3

sql_conn = sqlite3.connect('PhonePracticeDB.db')
cursor = sql_conn.cursor()

new_table = '''CREATE TABLE IF NOT EXISTS Entries2 (
                    EntriesID INTEGER PRIMARY KEY NOT NULL, 
                    FirstName TEXT, 
                    LastName TEXT, 
                    PhoneNumber TEXT NOT NULL, 
                    IsActive INTEGER NOT NULL DEFAULT 1)'''
cursor.execute(new_table)

set_auto_increment = 'ALTER TABLE Entries2 AUTOINCREMENT = 1'
cursor.execute(set_auto_increment)

new_record_1 = '''INSERT INTO Entries (FirstName, LastName, PhoneNumber)
                  VALUES ("Hikaru", "Sulu", "7775551111")'''

new_record_2 = '''INSERT INTO Entries (FirstName, LastName, PhoneNumber)
                  VALUES ("Montgomery", "Scott", "7775552222")'''

cursor.execute(new_record_2)
cursor.execute(new_record_1)

records = 'select* from Entries'
cursor.execute(records)
table_rows = cursor.fetchall()

for row in table_rows:
    print(row)

sql_conn.commit()
sql_conn.close()