import sqlite3
from datetime import datetime
from user import User

class Workout:
    def __init__(self, fitness_tracker):
        self.conn = sqlite3.connect(fitness_tracker)
        self.user = User(fitness_tracker)
        self.cursor = self.conn.cursor()

    def is_valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_workout(self, username, date, time):
        user_id = self.user.get_user_id(username)
        print(f"Adding workout for user_id: {user_id}, date: {date}, time: {time}")
        with self.conn:
            self.conn.execute(
                'INSERT INTO workouts (user_id, date, time) VALUES (?, ?, ?)',
                (user_id, date, time)
            )
            self.conn.commit()

    def list_workouts(self, username):
        user_id = self.user.get_user_id(username)
        if user_id is not None:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, date, time FROM workouts WHERE user_id = ?', (user_id,))
            workouts = cursor.fetchall()

            sorted_workouts = sorted(workouts, key=lambda x: x[1])

            return sorted_workouts
        else:
            print(f"{username} not found.")
            return []
        
    def delete_workout(self, workout_id):
        with self.conn:
            self.conn.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
            self.conn.commit()

    def get_workout_id(self, username, workout_date):
        query = """
            SELECT id
            FROM workouts
            WHERE user_id = ? AND date = ?
        """
        user_id = self.user.get_user_id(username)

        if user_id is None:
            return None

        values = (user_id, workout_date)
        self.cursor.execute(query, values)
        workout_id = self.cursor.fetchone()

        if workout_id:
            return workout_id[0]
        else:
            return None