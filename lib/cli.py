import click
from fitnesstracker import FitnessTracker

db_name = 'fitness_tracker.db'

@click.command()
def main():
    print_menu()

    while True:
        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            add_user()
            break
        elif choice == 2:
            log_in()
            break
        else:
            click.echo("Please select a valid option.")

def print_menu():
    with open("menu.txt", "r") as menu_file:
        menu_content = menu_file.read()
        click.echo(menu_content)

def add_user():
    tracker = FitnessTracker(db_name)
    username = click.prompt("Enter username")
    tracker.add_user(username)
    click.echo(f"Profile {username} was created.")

def log_in():
    tracker = FitnessTracker(db_name)
    username = click.prompt("Enter username")
    user_id = tracker.get_user_id(username)

    if user_id is not None:
        user_submenu(username)
    else:
        click.echo("Invalid username.")

def user_submenu(username):
    while True:
        print_user_submenu(username)

        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            option1(username)
        elif choice == 2:
            option2(username)
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