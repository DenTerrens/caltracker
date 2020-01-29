import json


NUTRITION = ['Proteins', 'Carbs', 'Fats', 'Calories']


def check_current():
    """Shows current day's consumed nutrition."""
    with open('data.json', 'r') as file:
        data = json.load(file)
    current_day = data["current_day"]

    for k, v in current_day.items():
        print(k + ":", v)


def reset_day():
    """Resets current day's values and deletes all items from eaten_today."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    for k in data["current_day"].keys():
        data["current_day"][k] = 0
    data["eaten_today"].clear()

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Values have been reset.")


def add_item(new_item, p=0, c=0, f=0, cal=0):
    """Adds consumed item with its name and nutrition values, updates current day's nutrition."""
    list_of_args = [p, c, f, cal]
    with open('data.json', 'r') as file:
        data = json.load(file)
    if new_item not in data["DATABASE"]:
        data["DATABASE"][new_item] = {}

        for i in NUTRITION:
            data["DATABASE"][new_item][i] = list_of_args[NUTRITION.index(i)]

    if new_item not in data["eaten_today"]:
        data["eaten_today"][new_item] = {}
        data["eaten_today"][new_item]["consumed"] = 1

        for i in NUTRITION:
            data["eaten_today"][new_item][i] = list_of_args[NUTRITION.index(i)]
            data["current_day"][i] += list_of_args[NUTRITION.index(i)]
        print(f"Added {new_item} to today's list.")

    else:
        data["eaten_today"][new_item]["consumed"] += 1

        for i in NUTRITION:
            data["eaten_today"][new_item][i] += list_of_args[NUTRITION.index(i)]
            data["current_day"][i] += list_of_args[NUTRITION.index(i)]
        print(f"Added one more of {new_item} to today's list.")

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def remove_item(existing_item):
    """Deletes an item from today's list of consumed items."""
    with open('data.json', 'r') as file:
        data = json.load(file)
    if existing_item not in data["eaten_today"]:
        print(f"Cannot remove {existing_item} as it is not in the list.")
    else:
        if data["eaten_today"][existing_item]["consumed"] > 1:
            data["eaten_today"][existing_item]["consumed"] -= 1

            for i in NUTRITION:
                data["eaten_today"][existing_item][i] -= data["DATABASE"][existing_item][i]

            for i in NUTRITION:
                data["current_day"][i] -= data["DATABASE"][existing_item][i]
            print(f"Removed 1 entry of {existing_item} from today's list.")

        else:
            data["eaten_today"].pop(existing_item)

            for i in NUTRITION:
                data["current_day"][i] -= data["DATABASE"][existing_item][i]
            print(f"Removed {existing_item} from today's list.")

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def show_items():
    """Displays all items consumed for the day."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    for k in data["eaten_today"].keys():
        print(f'{data["eaten_today"][k]["consumed"]} of {k}, \
total of {data["eaten_today"][k]["consumed"] * data["DATABASE"][k]["Calories"]} calories.')


def show_daily_needed():
    """Displays daily amount of nutrition needed to be consumed."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    for k in data["VALUES"].keys():
        print(f'{k}: {data["VALUES"][k]["daily"]}')


def show_left():
    """Displays what is left to be consumed for the day."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    for i in NUTRITION:
        print(f'{i}:', data["VALUES"][i]["daily"] - data["current_day"][i])


def show_commands():
    """Displays all available commands to the user."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    for k, v in data["commands"].items():
        print(f"{k.ljust(12)}- {v}")


def days_count():
    """Displays how many days the path is followed."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    return data['days_count']


def incr_days_count():
    """Increments days_count when a new day starts."""
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    data['days_count'] += 1

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def reset_days_count():
    """Resets days_count if user wants to restart progress."""
    with open('data.json', 'r') as file:
        data = json.load(file)

    data['days_count'] = 0

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
