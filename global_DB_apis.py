from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import requests
import json
import functions


def fatsecret(food):
    # client authorization, getting token
    client_id = '8f3d9de1df974e8d9c3452d131cd3187'
    client_secret = '9c8513c5e9de4daf8206b8c792273048'
    token_url = 'https://oauth.fatsecret.com/connect/token'

    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, auth=auth)

    # accessing FatSecret API - Search
    endpoint = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        'Authorization': "Bearer {0}".format(token["access_token"]),
    }
    data_search = {
        'method': 'foods.search',
        'search_expression': food,
        'format': 'json',
        'content-type': 'application/json'
    }
    r_search = requests.post(endpoint, headers=headers, data=data_search)
    j_search = json.loads(r_search.text)

    # list of results
    search = j_search['foods']['food']

    choice = ''
    choice_id = 0
    choices = {}
    for i in range(len(search)):
        if search[i]['food_type'] == 'Generic':
            words = search[i]['food_name'].lower().split(' ')
            for m in words:
                if m == food:
                    choices[search[i]['food_name']] = search[i]['food_id']
                    print(f"{i + 1} - {search[i]['food_name']}")

    while True:
        selected = input("\nSelect item (case sensitive): ").strip()
        if selected == 'q':
            break
        if selected not in choices:
            print("No such item, try again.")
        else:
            choice = selected
            choice_id = int(choices[choice])
            break

    data_get = {
        'method': 'food.get',
        'food_id': choice_id,
        'format': 'json',
        'content-type': 'application/json'
    }
    r_get = requests.post(endpoint, headers=headers, data=data_get)
    j_get = json.loads(r_get.text)
    get_servings = j_get['food']['servings']['serving']

    ids = []
    for i in range(len(get_servings)):
        ids.append(i + 1)

    serving_ids = {}
    for i in range(len(get_servings)):
        serving_ids[get_servings[i]['measurement_description']] = ids[i]
        print(f"{serving_ids[get_servings[i]['measurement_description']]} \
- {get_servings[i]['measurement_description']}")

    while True:
        serving = input("\nSelect serving (type its number): ").lower().strip()
        if serving == 'q':
            break
        if serving == '':
            print('Serving size must be specified.')
        else:
            try:
                serving = int(serving)
            except ValueError:
                print("Use serving's number only.")
            else:
                selected_serving = get_servings[serving]
                p = float(selected_serving['protein'])
                c = float(selected_serving['carbohydrate'])
                f = float(selected_serving['fat'])
                cal = float(selected_serving['calories'])
                serv = selected_serving
                choice = choice.lower()
                print(f"\nAdded {choice.lower()} from global to local database.")
                functions.add_item(choice, p=p, c=c, f=f, cal=cal)
                break
