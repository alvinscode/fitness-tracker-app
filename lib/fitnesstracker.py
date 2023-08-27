import sqlite3

class FitnessTracker:
    def __init__(self, fitness_tracker):
        self.conn = sqlite3.connect(fitness_tracker)