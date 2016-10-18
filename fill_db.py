# Fetch ingredient data from Spoonacular's Recipe - Food - Nutrition API
# Our developer key: aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh

import requests
from pprint import pprint

request_count = 1
recipes_per_request = 1

for x in range(0, request_count):

    payload = {'limitLicense': 'false', 
                'number': recipes_per_request}

    headers = {'X-Mashape-Key': 'aQIPLaXuVWmshofIutMCZ4MfTpeJp1cXtebjsn1YBY7nlBMgkh', 
                'Accept': 'application/json'}

    r = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/random', params=payload, headers=headers)
    print r.url

    json = r.json()
    
    #pprint(json)

    recipes = json["recipes"]

    for r in recipes:
        ingredients = r["extendedIngredients"]
        for i in ingredients:
            #pprint(i)
            ingredient_id = i["id"]
            name = i["name"]
            default_amount = i["amount"]
            aisle = i["aisle"]
            unit = i["unit"]
            unitShort = i["unitShort"]
            unitLong = i["unitLong"]
            metaInformation = i["metaInformation"]
            print name + ", id=" + str(ingredient_id) + ", unit=" + unit
