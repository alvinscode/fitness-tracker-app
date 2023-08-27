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
    
    def get_all_exercises_for_workout(self, workout_id):
        query = "SELECT * FROM exercises WHERE workout_id = ?"
        result = self.conn.execute(query, (workout_id,)).fetchall()
    
        exercises = []
        for row in result:
            exercise = {
                "id": row[0],
                "workout_id": row[1],
                "name": row[2],
                "sets": row[3],
                "reps": row[4],
                "weight": row[5]
            }
            exercises.append(exercise)
    
        return exercises

    def delete_exercise_by_id(self, exercise_id):
        query = "DELETE FROM exercises WHERE id = ?"
        self.conn.execute(query, (exercise_id,))
        self.conn.commit()