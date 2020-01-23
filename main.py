#!/usr/bin/env python3


import functions
import json


def main():
    # starting point
    print("Your current nutrition values:")
    functions.check_current()
    print("")
    print("Available commands:")
    functions.show_commands()

    # getting data loaded, more specifically - list of commands
    with open('data.json', 'r') as file:
        data = json.load(file)

    # getting user's initial input - main body of the program
    while True:
        action = input("\nEnter command to execute (enter 'q' anytime to exit program): ").lower().strip()
        if action == 'q':
            break
        if action not in data["commands"]:
            print(f"No such command. Please type 'commands' to see all available options.")
        else:
            # linking commands with actions
            if action == 'add':
                with open('data.json', 'r') as f:
                    database = json.load(f)
                # logic for adding new item to database vs getting that item from db into eaten today list
                while True:
                    new_item = input('\nName of product: ').lower().strip()
                    if new_item == '' or new_item == 'q':
                        break
                    if new_item not in database["DATABASE"]:
                        add_to_database = input(f'Could not find {new_item} in database, \
would you like to add one? (y/n) ').lower().strip()
                        if add_to_database == 'y':
                            p = int(input('\nProteins: ').strip())
                            c = int(input('Carbs: ').strip())
                            f = int(input('Fats: ').strip())
                            cal = int(input('Calories: ').strip())
                            print(f'Added {new_item} to the database.')
                            functions.add_item(new_item, p=p, c=c, f=f, cal=cal)
                            # if item added
                            break
                        else:
                            # if n selected, keep asking for a new item
                            continue
                    else:
                        functions.add_item(new_item, p=database["DATABASE"][new_item]["Proteins"],
                                           c=database["DATABASE"][new_item]["Carbs"],
                                           f=database["DATABASE"][new_item]["Fats"],
                                           cal=database["DATABASE"][new_item]["Calories"])
                        break

            elif action == 'remove':
                existing_item = input('Item to remove: ').lower().strip()
                functions.remove_item(existing_item)
            elif action == 'current':
                print('\nCurrent day values:')
                functions.check_current()
            elif action == 'reset':
                confirm_reset = input('Are you sure you want to reset? (y/n) ').lower().strip()
                if confirm_reset == 'y':
                    functions.reset_day()
            elif action == 'items':
                # checking if list of items is empty
                with open('data.json', 'r') as another_file:
                    another_data = json.load(another_file)
                if another_data['eaten_today'] != {}:
                    print('\nConsumed today:')
                    functions.show_items()
                else:
                    another_item = input("Today's list is empty. \
Would you like to add a new item? (y/n) ").lower().strip()
                    if another_item == 'y':
                        new_item = input('\nName of product: ').lower().strip()
                        p = int(input('Proteins: ').strip())
                        c = int(input('Carbs: ').strip())
                        f = int(input('Fats: ').strip())
                        cal = int(input('Calories: ').strip())
                        functions.add_item(new_item, p=p, c=c, f=f, cal=cal)
            elif action == 'daily':
                print('\nYour daily goal:')
                functions.show_daily_needed()
            elif action == 'left':
                print("\nLeft to achieve today's goal:")
                functions.show_left()
            elif action == 'commands':
                print('\nAvailable commands:')
                functions.show_commands()


if __name__ == '__main__':
    main()
