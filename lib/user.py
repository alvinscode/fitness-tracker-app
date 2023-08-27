import sqlite3

class User:
    def __init__(self, fitness_tracker):
        self.conn = sqlite3.connect(fitness_tracker)

    def add_user(self, username):
        existing_user = self.get_user_id(username)
        if existing_user is not None:
            print(f"'{username}' already exists. Try a different username.")
        else:
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
    
    def delete_user(self, username):
        with self.conn:
            self.conn.execute('DELETE FROM users WHERE username = ?', (username,))
            self.conn.commit()