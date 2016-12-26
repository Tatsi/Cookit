# Fetch ingredient data from Spoonacular's Recipe - Food - Nutrition API
# Our developer key: aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh

import requests
import datetime
from pprint import pprint
import json
import pickle

request_count = 10
recipes_per_request = 10
time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S").encode('utf-8')
data = []
counter = 1
ingredient_ids = []

with open('main/fixtures/ingredients_' + time + '.json', 'w') as outfile:
    for x in range(0, request_count):

        payload = {'limitLicense': 'false', 
                    'number': recipes_per_request}

        headers = {'X-Mashape-Key': 'aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh', 
                    'Accept': 'application/json'}

        r = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random', params=payload, headers=headers)
        jsontext = r.json()
        recipes = jsontext["recipes"]

        for r in recipes:
            ingredients = r["extendedIngredients"]
            
            for i in ingredients:
                if 'id' in i and 'aisle' in i:
                    ingredient_id = i["id"]
                    name = i["name"]
                    default_amount = i["amount"]
                    aisle = i["aisle"]
                    unit = i["unit"]
                    unitShort = i["unitShort"]
                    unitLong = i["unitLong"]
                    metaInformation = i["metaInformation"]
                    ingredient_ids.append(ingredient_id)

                    entry = dict(
                        model = 'main.ingredient',
                        pk = ingredient_id,
                        fields = dict(
                            ingredient_id = ingredient_id,
                            name = name,
                            default_amount = default_amount,
                            category = aisle,
                            unit = unit,
                            unit_short = unitShort,
                            unit_long = unitLong
                        )
                    )
                    data.append(entry)
                    counter += 1

    json.dump(data, outfile, indent = 4)

f = open("ingredient_ids", "w+b")
pickle.dump(ingredient_ids, f)
f.close()

