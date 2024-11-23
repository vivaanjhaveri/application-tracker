import sqlite3

# Function to connect to the database
def create_connection(db_file='applications.db'):
    conn = sqlite3.connect(db_file)
    return conn

# Function to create the applications table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        position TEXT NOT NULL,
        application_date TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table
create_table()
