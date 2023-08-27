# Fitness Tracker

## Introduction

Fitness Tracker is a CLI application that is designed to record workouts and
exercises for a user, while analyzing the data and providing insight on
the progress of workouts throughout time.

## cli.py

`cli.py` is the main entry point of the Fitness Tracker CLI application. It
will provide the user with a user-friendly menu system. From here, a user
will be able to create profiles, log in, add workouts, view workout details,
and manage exercises for those workouts.

## Functions and Models

### Important Functions

- `add_workout(self, username, date, time)`: This function will record a date and 
length of time for a workout for a user, the data will be saved and used for
analysis later on.

- `list_workouts_submenu(username)`: Depending on the user that is logged in, this
function will open a menu that will provide an extensive amount of details about 
the workouts that were entered. This function will show the date and length of the 
workouts, as well as every exercise that was done during that workout, with the 
sets, reps, and weight of that exercise shown as well. In addition to this, this 
function will also calculate the total and average reps of the exercise, as well 
as the total weight lifted. The average reps of the day is then compared with the 
previous day to generate a % difference, which will show if there is improvement 
or not with each workout. The total time of the workouts for the week will be shown 
as well, so the user will have an idea of how long they have spent working out 
throughout the week without having to calculate it themselves. Finally, a total weight 
number calculated to show the user if they have improved over the days.

- `add_exercise_submenu(username)`: This function will open a list of exercises to
allow the user to choose from. The user has the choice of creating their own custom
workout or making it entirely with a pre-made list of exercises. This function will
provides a very user-friendly interface for the user to design their workout and
document what they will be doing for a certain day.

- The rest of the functions in this CLI has a much less impact than the ones listed
above. There is a large variety of functions that will handle basic tasks like
recording the user, listing available profiles, deleting profiles, deleting
exercises, etc.

### Models

- `User`: This model represents the user profile. It includes attributes like `id`
and `username` will will be used to relate the user to a workout.
- `Workout`: This will represent each individual workout session. It will include
`id`, `user_id`, `date`, and `time`. The `id` and `user_id` are used to relate the
workout to the user and the exercises they will perform.
- `Exercise`: This represents each exercise that is performed in a workout. It will
include `id`, `workout_id`, `name`, `sets`, `reps`, and `weight`. The `workout_id`
attribute will create a relationship with the exercise and the workout, which is
ultimately linked to the user.

## Usage

To use the CLI, navigate to the project directory, then run these commands:

```pipenv install```
```cd lib```
```python cli.py```

## Dependencies

- SQLAlchemy: Used for database management and ORM functions.
- Click: Framework used to build the CLI.
- Python datetime module: Used to handle data that compares day to day changes.

## Resources

- [ASCII Art Generator that is used in the menus.](https://patorjk.com/software/taag/)

## Conclusion

The Fitness Tracker CLI provides an easy and convenient way to track your workout sessions 
and exercises. Whether you're a fitness enthusiast or simply looking to stay organized, 
this CLI offers a range of features to help you achieve your fitness goals.