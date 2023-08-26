from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    workouts = relationship('Workout', back_populates='user')

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(String, nullable=False)
    time = Column(String)
    user = relationship('User', back_populates='workouts')

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    workout_id= Column(Integer, ForeignKey('workouts.id'), nullable=False)
    name = Column(String, nullable=False)
    sets =  Column(Integer)
    reps = Column(Integer)
    weight = Column(Integer)
    workout = relationship('Workout', back_populates='exercises')