import sqlite3
from user import User
from workout import Workout

class Exercise:
    def __init__(self, fitness_tracker):
        self.conn = sqlite3.connect(fitness_tracker)
        self.user = User(fitness_tracker)
        self.workout = Workout(fitness_tracker)
        self.cursor = self.conn.cursor()

    def add_exercise(self, workout_id, name, sets, reps, weight):
        query = """
            INSERT INTO exercises (workout_id, name, sets, reps, weight)
            VALUES (?, ?, ?, ?, ?)
        """
        values = (workout_id, name, sets, reps, weight)

        self.cursor.execute(query, values)
        self.conn.commit()

    def view_exercises(self, workout_id):
        query = """
            SELECT name, sets, reps, weight
            FROM exercises
            WHERE workout_id = ?
        """
        values = (workout_id,)

        self.cursor.execute(query, values)
        exercises = self.cursor.fetchall()

        return exercises
    
    def get_exercise_by_id(self, exercise_id):
        query = "SELECT * FROM exercises WHERE id = ?"
        self.cursor.execute(query, (exercise_id,))
        exercise = self.cursor.fetchone()
        return exercise