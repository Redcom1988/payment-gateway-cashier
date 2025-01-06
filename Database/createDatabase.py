import os
import sqlite3

def createTables():
    if not os.path.exists('createTables.sql'):
        print(f"Error: createTables.sql not found!")
        return False

    conn = sqlite3.connect('store.db')

    with open('createTables.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    try:
        conn.executescript(sql_script)
        conn.commit()
        print("Database created successfully")
        return True
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        return False
    finally:
        conn.close()

def insertData():
    if not os.path.exists('insertDummy.sql'):
        print(f"Error: insertDummy.sql not found!")
        return False

    conn = sqlite3.connect('store.db')

    with open('insertDummy.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    try: 
        conn.executescript(sql_script)
        conn.commit()
        print("Data inserted successfully")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

def print_debug_info():
    print(f"Debug Information:")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    print("----------------------------------------")

def main():
    # print_debug_info()
    if createTables():
        insertData()

if __name__ == '__main__':
    main()