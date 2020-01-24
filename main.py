#!/usr/bin/env python3


import functions
import json


NUTRITION = ['Proteins', 'Carbs', 'Fats', 'Calories']


def main():
    # starting point
    print("Your current nutrition values:")
    functions.check_current()
    print("")
    print("Available commands:")
    functions.show_commands()

    # getting user's initial input - main body of the program
    while True:
        action = input("\nEnter command (enter 'q' anytime to exit program): ").lower().strip().split(' ')
        if action[0] == 'q':
            break
        # getting data loaded, more specifically - list of commands
        with open('data.json', 'r') as file:
            data = json.load(file)
        if action[0] not in data["commands"]:
            print("No such command. Type 'commands' to see all available options.")
        else:
            # linking commands with actions
            if action[0] == 'add':
                if len(action) != 2:
                    print("Usage: add item_name")
                    continue
                with open('data.json', 'r') as f:
                    database = json.load(f)
                # logic for adding new item to database vs getting that item from db into eaten today list
                new_item = action[1]
                if new_item not in database["DATABASE"]:
                    add_to_database = input(f'Unable to find {new_item} in the database, \
would you like to add it? (y/n) ').lower().strip()
                    if add_to_database == 'q':
                        continue
                    if add_to_database == 'y':
                        p, c, f, cal = '', '', '', ''
                        nutr = [p, c, f, cal]
                        exit_flag = False  # flag to avoid the need to enter all 4 values if one of them was quit
                        not_all_four = False  # flag to prohibit values to go into database if not all 4 were entered
                        exited = False  # flag to avoid displaying a message that all 4 values are needed
                        for i in NUTRITION:
                            if exit_flag:
                                break
                            while True:
                                nutr[NUTRITION.index(i)] = input(f"{i}: ").strip()
                                # changes flags which results in returning to main entry field
                                if nutr[NUTRITION.index(i)] == 'q':
                                    exit_flag = True
                                    not_all_four = True
                                    exited = True
                                    break
                                if nutr[NUTRITION.index(i)] == '':
                                    print("Cannot skip values. Enter 0 for empty value.")
                                else:
                                    try:
                                        nutr[NUTRITION.index(i)] = int(nutr[NUTRITION.index(i)])
                                    except ValueError:
                                        print("Please use only digits.")
                                    else:
                                        break
                        if not exited:
                            # the following condition is questionable, I will leave it here for now just in case
                            # ...'cause it's working :D
                            if not_all_four:
                                print("Need all 4 nutrition values to continue.")
                            else:
                                functions.add_item(new_item, p=nutr[0], c=nutr[1], f=nutr[2], cal=nutr[3])
                                print(f'Added {new_item} to the database.')
                    else:
                        continue

                else:
                    functions.add_item(new_item, p=database["DATABASE"][new_item]["Proteins"],
                                       c=database["DATABASE"][new_item]["Carbs"],
                                       f=database["DATABASE"][new_item]["Fats"],
                                       cal=database["DATABASE"][new_item]["Calories"])

            elif action[0] == 'remove':
                if len(action) != 2:
                    print("Usage: remove item_name")
                    continue
                existing_item = action[1]
                functions.remove_item(existing_item)
            elif action[0] == 'current':
                print('\nCurrent day values:')
                functions.check_current()
            elif action[0] == 'reset':
                confirm_reset = input('Are you sure you want to reset? (y/n) ').lower().strip()
                if confirm_reset == 'q':
                    continue
                if confirm_reset == 'y':
                    functions.reset_day()
            elif action[0] == 'items':
                # checking if list of items is empty
                with open('data.json', 'r') as another_file:
                    another_data = json.load(another_file)
                if another_data['eaten_today'] != {}:
                    print('\nConsumed today:')
                    functions.show_items()
                else:
                    another_item = input("Today's list is empty. Would you like to add a new item? \
(y/n) ").lower().strip()
                    if another_item == 'q':
                        continue
                    if another_item == 'y':
                        exit_choosing_product = False  # flag to exit to main entry field after adding a new item
                        while True:
                            if exit_choosing_product:
                                break
                            new_item = input('\nName of product: ').lower().strip()
                            if new_item == 'q':
                                break
                            if new_item not in another_data["DATABASE"]:
                                add_to_database = input(f'Could not find {new_item} in database, \
would you like to add one? (y/n) ').lower().strip()
                                if add_to_database == 'q':
                                    break
                                if add_to_database == 'y':
                                    # below is a very close replication of the above condition but with 1 more flag
                                    # may be optimized later if needed
                                    p, c, f, cal = '', '', '', ''
                                    nutr = [p, c, f, cal]
                                    exit_flag = False
                                    not_all_four = False
                                    exited = False
                                    for i in NUTRITION:
                                        if exit_flag:
                                            break
                                        while True:
                                            nutr[NUTRITION.index(i)] = input(f"{i}: ").strip()
                                            if nutr[NUTRITION.index(i)] == 'q':
                                                exit_flag = True
                                                not_all_four = True
                                                exited = True
                                                exit_choosing_product = True
                                                break
                                            if nutr[NUTRITION.index(i)] == '':
                                                print("Cannot skip values. Enter 0 for empty value.")
                                            else:
                                                try:
                                                    nutr[NUTRITION.index(i)] = int(nutr[NUTRITION.index(i)])
                                                except ValueError:
                                                    print("Please use only digits.")
                                                else:
                                                    break
                                    if not exited:
                                        if not_all_four:
                                            print("Need all 4 nutrition values to continue.")
                                        else:
                                            functions.add_item(new_item, p=nutr[0], c=nutr[1], f=nutr[2], cal=nutr[3])
                                            print(f'Added {new_item} to the database.')
                                            exit_choosing_product = True
                                else:
                                    continue
                            else:
                                functions.add_item(new_item, p=another_data["DATABASE"][new_item]["Proteins"],
                                                   c=another_data["DATABASE"][new_item]["Carbs"],
                                                   f=another_data["DATABASE"][new_item]["Fats"],
                                                   cal=another_data["DATABASE"][new_item]["Calories"])
                                break

            elif action[0] == 'daily':
                print('\nYour daily goal:')
                functions.show_daily_needed()
            elif action[0] == 'left':
                print("\nLeft to achieve today's goal:")
                functions.show_left()
            elif action[0] == 'commands':
                print('\nAvailable commands:')
                functions.show_commands()


if __name__ == '__main__':
    main()
