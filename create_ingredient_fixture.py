# Fetch ingredient data from Spoonacular's Recipe - Food - Nutrition API
# Our developer key: aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh

import requests
import datetime
from pprint import pprint
import json

request_count = 10
recipes_per_request = 10
time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S").encode('utf-8')

with open('main/fixtures/ingredients_' + time + '.json', 'w') as outfile:
    for x in range(0, request_count):

        payload = {'limitLicense': 'false', 
                    'number': recipes_per_request}

        headers = {'X-Mashape-Key': 'aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh', 
                    'Accept': 'application/json'}

        r = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random', params=payload, headers=headers)
        #print r.url
        jsontext = r.json()
        #pprint(jsontext)
        recipes = jsontext["recipes"]

        for r in recipes:
            ingredients = r["extendedIngredients"]
            data = []

            for i in ingredients:
                #pprint(i)
                if 'id' in i and 'aisle' in i:
                    ingredient_id = i["id"]
                    name = i["name"]
                    default_amount = i["amount"]
                    aisle = i["aisle"]
                    unit = i["unit"]
                    unitShort = i["unitShort"]
                    unitLong = i["unitLong"]
                    metaInformation = i["metaInformation"]
                    # print name + ", id=" + str(ingredient_id) + ", unit=" + unit

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
                            unit_long = unitLong,
                            meta_information = metaInformation
                        )
                    )
                    data.append(entry)
            json.dump(data, outfile, indent = 4)

