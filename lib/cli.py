import click
import os
import platform
from fitnesstracker import FitnessTracker

db = 'fitness_tracker.db'

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

def add_user():
    while True:
        clear_console()
        username = click.prompt("Enter username (Enter 'back' to return to main menu)")

        if username.lower() == 'back':
            main()
        else:
            tracker = FitnessTracker(db)
            tracker.add_user(username)
            click.echo(f"Profile {username} was created.")

def log_in():
    tracker = FitnessTracker(db)
    username = click.prompt("Enter username (Enter 'back' to return to main menu)")

    user_id = tracker.get_user_id(username)

    if user_id is not None:
        user_submenu(username)
    elif user_id.lower() == 'back':
        main()
    else:
        click.echo("Invalid username.")
        log_in()

def list_all_users():
    tracker = FitnessTracker(db)
    users = tracker.get_all_users()

    click.echo("Available Profiles:")
    for user in users:
        click.echo(user[1])

def user_submenu(username):
    while True:
        clear_console()
        print_user_submenu(username)

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            add_workout(username)
            break
        elif choice == 2:
            list_workouts(username)
            break
        else:
            click.echo("Please select a valid option.")

def print_user_submenu(username):
    click.echo(f"Welcome, {username}.")
    click.echo("1. Add Workout")
    click.echo("2. List All Workouts")

def add_workout(username):
    clear_console()
    date = click.prompt("Enter workout date (YYYY-MM-DD)")

    tracker = FitnessTracker(db)
    tracker.add_workout(username, date)

def list_workouts(username):
    tracker = FitnessTracker(db)
    workouts = tracker.list_workouts(username)
    
    if workouts:
        click.echo(f"Workouts for {username}:")
        for workout in workouts:
            click.echo(workout)
    else:
        click.echo(f"No workouts found for {username}.")

if __name__ == '__main__':
    main()