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


        
