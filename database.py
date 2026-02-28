# import sqlite3

# def init_db():
#     conn = sqlite3.connect('hospital.db')
#     cursor = conn.cursor()

#     # Create Patients Table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS patients (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             age INTEGER,
#             blood_group TEXT,
#             condition TEXT,
#             doctor TEXT,
#             status TEXT,
#             admission_date TEXT
#         )
#     ''')

#     # Create Doctors Table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS doctors (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             specialty TEXT,
#             availability TEXT,
#             schedule TEXT
#         )
#     ''')

#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     init_db()
#     print("Database initialized successfully.")


import sqlite3

def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # 1. Create Patients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            blood_group TEXT,
            condition TEXT,
            doctor TEXT,
            status TEXT,
            admission_date TEXT
        )
    ''')

    # 2. Create Doctors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty TEXT,
            availability TEXT,
            schedule TEXT
        )
    ''')

    # 3. Create Chat History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_res TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # create appointment table 
    conn.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized with all tables: patients, doctors, chat_history.")

def log_interaction(user_msg, bot_res):
    """Saves a chatbot conversation to the database."""
    conn = sqlite3.connect('hospital.db')
    conn.execute('INSERT INTO chat_history (user_msg, bot_res) VALUES (?, ?)', 
                 (user_msg, bot_res))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()