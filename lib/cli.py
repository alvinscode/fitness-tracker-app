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
    tracker = FitnessTracker(db)
    username = click.prompt("Enter username")
    tracker.add_user(username)
    click.echo(f"Profile {username} was created.")

def log_in():
    tracker = FitnessTracker(db)
    username = click.prompt("Enter username")
    user_id = tracker.get_user_id(username)

    if user_id is not None:
        user_submenu(username)
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
            option1(username)
            break
        elif choice == 2:
            option2(username)
            break
        else:
            click.echo("Please select a valid option.")

def print_user_submenu(username):
    click.echo(f"Welcome, {username}.")
    click.echo("1. Option 1")
    click.echo("2. Option 2")

def option1(username):
    click.echo(f"{username} selected Option 1.")

def option2(username):
    click.echo(f"{username} selected Option 2.")

if __name__ == '__main__':
    main()