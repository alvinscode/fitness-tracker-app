import click
import os
import platform
import datetime
from user import User
from workout import Workout
from exercise import Exercise

db = 'db/fitness_tracker.db'

exercise_names = ["Bench Press", "Bicep Curls", "Cable Chest Fly", "Dumbbell Overhead Extension", "Incline Bench Press", "Pull Ups", "Face Pulls", "Crunches", "Russian Twists", "Leg Raise + Toe Touch", "Reach Thru Crunches", "L-Sit Toe Touches", "Oblique Heel Taps", "Russian Twists", "Mountain Climbers"]

def clear_console():
    system = platform.system()
    if system == "Windows":
       os.system("cls")
    else:
        os.system("clear")

@click.command()
def main():
    clear_console()
    print_menu()

    while True:
        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            clear_console()
            add_user()
            break
        elif choice == 2:
            clear_console()
            log_in()
            break
        elif choice == 3:
            clear_console()
            list_all_users()
            log_in()
            break
        elif choice == 4:
            break
        else:
            click.echo("Please select a valid option.")

def print_menu():
    with open("menu.txt", "r") as menu_file:
        menu_content = menu_file.read()
        click.echo(menu_content)
        click.echo()
        click.echo("Main Menu")
        click.echo()
        click.echo("1. Create Profile")
        click.echo("2. Log In")
        click.echo("3. List All Profiles")
        click.echo("4. Exit Main Menu")
        click.echo()

def add_user():
    while True:
        username = click.prompt("Enter profile username (Enter 'back' to return to main menu)")

        if username.lower() == 'back':
            main()
            break
        else:
            tracker = User(db)
            existing_user = tracker.get_user_id(username)
            if existing_user is not None:
                print(f"{username} already exists. Please choose a unique username.")
            else:
                tracker.add_user(username)
                click.echo(f"Profile {username} was created.")
                input("Press Enter to continue...")
                main()
                break

def log_in():
    tracker = User(db)
    username = click.prompt("Enter profile username (Enter 'back' to return to main menu)")

    user_id = tracker.get_user_id(username)

    if user_id is not None:
        user_submenu(username)
    elif username.lower() == 'back':
        main()
    else:
        click.echo("Invalid username.")
        log_in()

def list_all_users():
    tracker = User(db)
    users = tracker.get_all_users()

    click.echo("Available Profiles:")
    for user in users:
        click.echo(user[1])

def user_submenu(username):
    clear_console()
    print_user_submenu(username)
    
    while True:
        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            add_workout_submenu(username)
            break
        elif choice == 2:
            list_workouts_submenu(username)
        elif choice == 3:
            select_workout_date(username)
        elif choice == 4:
            delete_workouts_submenu(username)
            break
        elif choice == 5:
            delete_user_submenu(username)
            break
        elif choice == 6:
            main()
            break
        else:
            click.echo("Please select a valid option.")

def print_user_submenu(username):
    with open("menu.txt", "r") as menu_file:
        menu_content = menu_file.read()
        click.echo(menu_content)
    click.echo()
    click.echo(f"Welcome, {username}.")
    click.echo()
    click.echo("1. Add Workout")
    click.echo("2. View Workout Details")
    click.echo("3. Select Workout")
    click.echo("4. Delete Workout")
    click.echo("5. Delete Profile")
    click.echo("6. Log Out (Return to Main Menu)")
    click.echo()

def add_workout_submenu(username):
    clear_console()
    while True:
        date = click.prompt("Enter workout date (YYYY-MM-DD) or '0' to cancel")
        print(f"Collected date: {date}")
        
        if date == '0':
            click.echo("Workout addition cancelled.")
            input("Press Enter to continue...")
            user_submenu(username)
            break
        
        time = click.prompt("Enter workout length (HH:MM) or '0' to cancel")
        print(f"Collected time: {time}")

        if time == '0':
            click.echo("Workout addition cancelled.")
            input("Press Enter to continue...")
            user_submenu(username)
            break
        
        try:
            workout_time = datetime.datetime.strptime(time, '%H:%M')
        except ValueError:
            click.echo("Invalid time format. Use HH:MM format.")
            continue

        tracker = Workout(db)
        if not tracker.is_valid_date(date):
            click.echo("Invalid date format. Use (YYYY-MM-DD) format.")
            continue

        tracker.add_workout(username, date, time)
        click.echo(f"Workout added for {username} on {date} at {time}.")
        input("Press Enter to continue...")
        user_submenu(username)
        break

def select_workout_date(username):
    clear_console()

    tracker = Workout(db)
    workouts = tracker.list_workouts(username)

    if not workouts:
        click.echo(f"No workouts found for {username}.")
        input("Press Enter to continue...")
        user_submenu(username)
        return
    
    click.echo("Select a workout:")
    click.echo()
    for idx, workout in enumerate(workouts, start=1):
        click.echo(f"{idx}. Workout on {workout[1]} for {workout[2]}")
    click.echo()
    
    choice = click.prompt("Enter the number of the date you wish to select (Enter '0' to cancel)", type=int)

    if choice == 0:
        click.echo("Workout selection cancelled.")
        input("Press Enter to continue...")
        user_submenu(username)
    elif 1 <= choice <= len(workouts):
        selected_workout = workouts[choice - 1]
        workout_date = selected_workout[1]

        exercises_menu(username, workout_date, exercise_names)
    else:
        click.echo("Please select a valid option.")
        input("Press Enter to continue...")
        select_workout_date(username)

def list_workouts_submenu(username):
    clear_console()
    tracker = Workout(db)
    workouts = tracker.list_workouts(username)
    
    if workouts:
        click.echo(f"Workouts for {username}:")
        click.echo()

        exercisetracker = Exercise(db)
        total_week_time = datetime.timedelta()
        total_week_weight = 0
        last_day_total_reps = None
        last_day_total_weight = None

        for idx, workout in enumerate(workouts):
            workout_id = workout[0]
            workout_date = datetime.datetime.strptime(workout[1], '%Y-%m-%d')
            days_since_workout = (datetime.datetime.now() - workout_date).days

            if days_since_workout <= 7:
                exercises = exercisetracker.get_all_exercises_for_workout(workout_id)
                total_reps = sum(exercise['reps'] * exercise['sets'] for exercise in exercises)
                average_reps = total_reps / len(exercises) if len(exercises) > 0 else 0
                total_weight = sum(exercise['weight'] for exercise in exercises)

                if exercises:
                    click.echo(f"Date: {workout[1]} | Total Workout Time: {workout[2]}")
                    click.echo("Exercises:")
                    for exercise in exercises:
                        click.echo(f"- {exercise['name']} - Sets: {exercise['sets']}, Reps: {exercise['reps']}, Weight: {exercise['weight']} lbs")

                    click.echo(f"Total Reps: {total_reps} | Average Reps: {average_reps:.2f}")
                    click.echo(f"Total Weight Lifted: {total_weight} lbs.")

                    workout_time = datetime.datetime.strptime(workout[2], '%H:%M')
                    total_time = datetime.timedelta(hours=workout_time.hour, minutes=workout_time.minute)
                    click.echo()

                    total_week_time += total_time
                    total_week_weight += total_weight

                    if idx > 0 and last_day_total_reps is not None:
                        daily_reps_improvement = ((total_reps - last_day_total_reps) / last_day_total_reps) * 100
                        click.echo(f"Daily Rep Improvement: {daily_reps_improvement:.2f}%")

                    if idx > 0 and last_day_total_weight is not None and last_day_total_weight != 0:
                        daily_weight_improvement = ((total_weight - last_day_total_weight) / last_day_total_weight) * 100
                        click.echo(f"Daily Weight Improvement: {daily_weight_improvement:.2f}%")

                    last_day_total_reps = total_reps
                    last_day_total_weight = total_weight

        click.echo(f"Total Time for the Week: {total_week_time}")
        click.echo(f"Total Weight Lifted for the Week: {total_week_weight} lbs.")

    else:
        click.echo(f"No workouts found for {username}.")

    click.echo()
    input("Press Enter to continue...")
    user_submenu(username)

def delete_workouts_submenu(username):
    clear_console()
    tracker = Workout(db)

    while True:
        workouts = tracker.list_workouts(username)

        if not workouts:
            click.echo(f"No workouts found for {username}.")
            input("Press Enter to continue...")
            user_submenu(username)
    
        click.echo(f"Workouts for {username}:")
        click.echo()
        for idx, workout in enumerate(workouts, start=1):
            click.echo(f"{idx}. Date: {workout[1]} | Workout Time: {workout[2]}")
        
        click.echo()
        choice = click.prompt("Select a workout to delete (Enter '0' to cancel deletion)", type=int)
        if choice == 0:
            click.echo("Deletion was cancelled.")
            break
        elif 1 <= choice <= len(workouts):
            workout_to_delete = workouts[choice - 1]
            workout_id = tracker.get_workout_id(username, workout_to_delete[1])

            confirmed = click.confirm(f"Are you sure you want to delete this workout: '{workout_to_delete[1]} - {workout_to_delete[2]}'?")

            if confirmed:
                tracker.delete_workout(workout_id)
                click.echo(f"Workout: {workout_to_delete[1]} - {workout_to_delete[2]} has been deleted.")
                input("Press Enter to continue...")
                break
            else:
                click.echo("Deletion was cancelled.")
                break
        else:
            click.echo("Please select a valid option.")

    user_submenu(username)

def delete_user_submenu(username):
    tracker = User(db)
    confirmed = click.confirm(f"Are you sure you want to delete profile '{username}'?")

    if confirmed:
        tracker.delete_user(username)
        click.echo(f"'{username}' has been deleted.")
        input("Press Enter to continue...")
        main()

    else:
        click.echo("Deletion was cancelled.")
        input("Press Enter to continue...")
        user_submenu(username)
        
    


def exercises_menu(username, workout_date, exercise_names):
    clear_console()
    print_exercises_menu(username, workout_date)

    while True:
        choice = click.prompt("Select an option", type=int)
    
        if choice == 1:
            add_exercise_submenu(username, workout_date, exercise_names)
            break
        elif choice == 2:
            view_exercises(username, workout_date)
        elif choice == 3:
            delete_exercise_menu(username, workout_date)
        elif choice == 4:
            user_submenu(username)
        else:
            click.echo("Please select a valid option.")

def print_exercises_menu(username, workout_date):
    with open("menu.txt", "r") as menu_file:
        menu_content = menu_file.read()
        click.echo(menu_content)
    click.echo()
    click.echo(f"Would you like to add or change exercises to your workout on {workout_date}, {username}?:")
    click.echo()
    click.echo("1. Add Exercise")
    click.echo("2. View Exercises")
    click.echo("3. Delete Exercise")
    click.echo("4. Go Back")
    click.echo()

def add_exercise_submenu(username, workout_date, exercise_names):
    clear_console()

    tracker = Workout(db)
    workout_id = tracker.get_workout_id(username, workout_date)

    if workout_id is None:
        click.echo(f"No workout found for {username} on {workout_date}.")
    else:
        click.echo(f"Adding exercise for {username} on {workout_date}")
        click.echo("Available exercise names:")
        for idx, name in enumerate(exercise_names, start=1):
            click.echo(f"{idx}. {name}")

        exercise_name_idx = click.prompt("Enter the number of the exercise name (Enter 'back' to go back or 'custom' to enter a custom exercise)", type=str)

        if exercise_name_idx.lower() == 'back':
            exercises_menu(username, workout_date, exercise_names)
            return
        elif exercise_name_idx.lower() == 'custom':
            exercise_name = click.prompt("Enter custom exercise name")
        else:
            exercise_name_idx = int(exercise_name_idx)
            if 1 <= exercise_name_idx <= len(exercise_names):
                exercise_name = exercise_names[exercise_name_idx - 1]
            else:
                click.echo("Invalid exercise name number.")
                input("Press Enter to continue...")
                add_exercise_submenu(username, workout_date, exercise_names)
                return

        sets = click.prompt("Enter number of sets (Enter '-1' to go back)", type=int)
        if sets == -1:
            exercises_menu(username, workout_date, exercise_names)

        reps = click.prompt("Enter number of reps (Enter '-1' to go back)", type=int)
        if reps == -1:
            exercise_name(username, workout_date, exercise_names)

        weight = click.prompt("Enter weight (Enter '-1' to go back)", type=int)
        if weight == -1:
            exercise_name(username, workout_date, exercise_names)

        exercise_tracker = Exercise(db)
        exercise_tracker.add_exercise(workout_id, exercise_name, sets, reps, weight)

        click.echo("Exercise added successfully.")
        input("Press Enter to continue...")
        exercises_menu(username, workout_date, exercise_names)

def view_exercises(username, workout_date):
    clear_console()
    click.echo(f"Displaying all exercises for {username} on {workout_date}...")

    workouttracker = Workout(db)
    exercisetracker = Exercise(db)
    workout_id = workouttracker.get_workout_id(username, workout_date)

    if workout_id is None:
        click.echo(f"No workout found for {username} on {workout_date}.")
        return

    exercises = exercisetracker.view_exercises(workout_id)

    if exercises:
        click.echo()
        click.echo(f"{'Name':<30}{'Sets':<10}{'Reps':<10}{'Weight':<10}")
        click.echo("=" * 60)

        for exercise in exercises:
            name, sets, reps, weight = exercise
            click.echo(f"{name:<30}{sets:<10}{reps:<10}{weight:<10}")
    else:
        click.echo("No exercises found for this workout.")

    click.echo()
    input("Press Enter to continue...")
    exercises_menu(username, workout_date, exercise_names)

def delete_exercise_menu(username, workout_date):
    clear_console()

    workouttracker = Workout(db)
    exercisetracker = Exercise(db)
    workout_id = workouttracker.get_workout_id(username, workout_date)

    if workout_id is None:
        click.echo(f"No workout found for {username} on {workout_date}.")
        input("Press Enter to continue...")
        exercises_menu(username, workout_date)
        return

    exercises = exercisetracker.get_all_exercises_for_workout(workout_id)

    if not exercises:
        click.echo("No exercises available to delete.")
        input("Press Enter to continue...")
        exercises_menu(username, workout_date)
        return

    click.echo("Select an exercise to delete:")
    click.echo()
    for idx, exercise in enumerate(exercises, start=1):
        click.echo(f"{idx}. {exercise['name']} - Sets: {exercise['sets']}, Reps: {exercise['reps']}, Weight: {exercise['weight']}")

    click.echo()
    choice = click.prompt("Enter the number of the exercise you wish to delete (Enter '0' to cancel)", type=int)
    click.echo()

    if choice == 0:
        click.echo("Exercise deletion cancelled.")
    elif 1 <= choice <= len(exercises):
        exercise_to_delete = exercises[choice - 1]
        exercise_id = exercise_to_delete['id']

        confirmed = click.confirm(f"Are you sure you want to delete this exercise: '{exercise_to_delete['name']}'?")

        if confirmed:
            exercisetracker.delete_exercise_by_id(exercise_id)
            click.echo(f"Exercise '{exercise_to_delete['name']}' has been deleted.")
        else:
            click.echo("Exercise deletion was cancelled.")

        exercisetracker.conn.close()
    else:
        click.echo("Invalid input.")

    input("Press Enter to continue...")
    exercises_menu(username, workout_date)

if __name__ == '__main__':
    main()