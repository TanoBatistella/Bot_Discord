import sqlite3
from datetime import datetime

def create_table():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS greetings (
                user_id INTEGER PRIMARY KEY,
                last_greeting_date TEXT
            )
        ''')
        conn.commit()

def get_last_greeting(user_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT last_greeting_date FROM greetings WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        return result[0] if result else None

def update_last_greeting(user_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO greetings (user_id, last_greeting_date)
            VALUES (?, ?)
        ''', (user_id, datetime.now().date().isoformat()))
        conn.commit()
