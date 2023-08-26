import sqlite3

class FitnessTracker:
    def __init__(self, fitness_tracker):
        self.conn = sqlite3.connect(fitness_tracker)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL
                )
            ''')

    def add_user(self, username):
        with self.conn:
            self.conn.execute('INSERT INTO users (username) VALUES (?)', (username,))
            self.conn.commit()

    def get_user_id(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()
        return user_id[0] if user_id else None
    
    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * from users')
        users = cursor.fetchall()
        return users


        
