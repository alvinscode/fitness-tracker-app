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

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
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

    def add_workout(self, username, date):
        user_id = self.get_user_id(username)
        if user_id is not None:
            with self.conn:
                self.conn.execute('INSERT INTO workouts (user_id, date) VALUES (?, ?)', (user_id, date))
                self.conn.commit()
                print(f"Workout added for {username} on {date}.")

        else:
            print(f"{username} not found.")

    def list_workouts(self, username):
        user_id = self.get_user_id(username)
        if user_id is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT date FROM workouts WHERE user_id = ?', (user_id,))
            workouts = cursor.fetchall()
            return [workout[0] for workout in workouts]
        else:
            print(f"{username} not found.")
            return []
