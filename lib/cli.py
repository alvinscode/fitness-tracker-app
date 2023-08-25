import click

@click.command()
def main():
    print_menu()

    while True:
        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            option1()
            break
        elif choice == 2:
            option2()
            break
        else:
            click.echo("Please select a valid option.")

def print_menu():
    with open("menu.txt", "r") as menu_file:
        menu_content = menu_file.read()
        click.echo(menu_content)

def option1():
    click.echo("Option 1 selected.")

def option2():
    click.echo("Option 2 selected.")

if __name__ == '__main__':
    main()