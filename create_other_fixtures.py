# Create testing data fixtures to main/fixtures. The created fixture file contains examples of all other
# models than ingredients.
# The fixture can be loaded with command: python manage.py loaddata main/fixtures/<filename>

from pprint import pprint
import json
import datetime
from random import sample, randint

time = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S").encode('utf-8')
data = []

with open('main/fixtures/others_' + time + '.json', 'w') as outfile:
    for i in range(1, 11):
        username = "user" + str(i)
        email = "user" + str(i) + "@cookit.com"
        is_super_user = False

        if (i == 1):
            is_super_user = True

        # Create User 1-10 fixtures. These have been made with django admin and dumped to a file with command:
        # python manage.py dumpdata auth.User --indent 4 > file
        # Then the text is used to create several users with the same hash.
        # Usernames are user1-user10 and passwords are "password". user1 is a superuser
        entry = dict(
            model = 'auth.user',
            pk = i,
            fields = dict(
                password = "pbkdf2_sha256$30000$qwdCTXISuS1t$CyHx8U8Q7b/JlX24lOqbUXm+n2BrwNfHVzqNL3GkWs4=",
                last_login = "2016-11-09T18:08:23.137Z",
                is_superuser = is_super_user,
                username = username,
                first_name = "",
                last_name = "",
                email = email,
                is_staff = is_super_user,
                is_active = True,
                date_joined = "2016-11-09T18:08:13.734Z",
                groups = [],
                user_permissions = []
            )
        )
        data.append(entry)

        # Create UserAccount 1-10 fixtures with links to previous users
        favourite_recipes = range(1, i)
        favourite_users = range(1, i)
        history_recipes = range(10 * (i-1) + 1, 8 + 10 * (i - 1) + 1 )
        ingredients = range(10 * (i-1) + 1, 8 + 10 * (i - 1) + 1 )

        # Create the actual User Accounts
        entry = dict(
            model = 'main.useraccount',
            pk = i,
            fields = dict(
                user = i,
                favourite_users = favourite_users,
                favourite_recipes = favourite_recipes,
                description = """Internationally renowned, multi-Michelin starred chef Gordon Ramsay has opened a string of successful restaurants across the globe, from the UK and France to Singapore and Hong Kong, to the United States. Gordon has also become a star of the small screen both in the UK and internationally, with shows such as Kitchen Nightmares, Hell's Kitchen, Hotel Hell and MasterChef US.""",
            )
        )
        data.append(entry)

        # Create the related UserIngredients
        max_user_ingredients_per_user = 30
        ingredient_count = randint(5, max_user_ingredients_per_user)
        random_ingredients = sample(xrange(1, 950), ingredient_count)
        for x in random_ingredients:
            entry = dict(
                model = 'main.useringredient',
                pk = (i - 1) * max_user_ingredients_per_user + x,
                fields = dict(
                    user_account = i,
                    ingredient = x,
                    amount = randint(4, 20),
                    infinite = False
                )
            )
            data.append(entry)

        # Create the related HistoryRecipes
        for j in range(1,4):
            entry = dict(
                model = 'main.cookedrecipe',
                pk = x,
                fields = dict(
                    recipe = str((i-1) * 3 + j-1),
                    user_account = i,
                    cooking_date = "2016-02-02",
                    cooking_time = "09:23:15",
                    serving_count = str(x + 1)
                )
            )
            data.append(entry)

        # Create 3 Recipe entries for each user
        hours = randint(0, 4)
        minutes = randint(0, 59)
        duration = datetime.timedelta(hours=hours, minutes=minutes)
        image_url = "www.example.com/image.png"
        steps = [
            "Take all the ingredients in front of you.",
            "Start by slicing the vegetables and the meat.",
            "Season the ingredients with pepper.",
            "Wash your hands and make sure your kitchen and tools are clean.",
            "Mix them and season with salt and pepper.",
            "Heat the water and add some salt to it.",
            "Fry them in a frying pan for 20 minutes.",
            "Roll the pastry in big rolls.",
            "Enjoy your delicious meal!",
            "Put it in the oven for 30 minutes."
            "Add some vinegar",
            "Wash the salad and other vegetables",
            "Deep fry the seasoned chicken legs",
            "Mash the ingredients into a paste. Add some water if it gets too thick",
            "Boil the eggs for 8-9 minutes. Make sure not to boil them for any longer!",
            "Preheat oven to 375 degrees F (190 degrees C).",
            "Pour beaten eggs into a shallow dish or bowl. In another shallow dish or bowl, mix together the grated Parmesan cheese and bread crumbs. Dip chicken breasts into beaten egg, then into bread crumb mixture to coat.",
            "In a large skillet, heat oil over medium high heat. Add coated chicken and saute for about 8 to 10 minutes each side, or until chicken is cooked through and juices run clear.",
            "Pour tomato sauce into a lightly greased 9x13 inch baking dish. Add chicken, then place a slice of Monterey Jack cheese over each breast, and bake in the preheated oven for 20 minutes or until cheese is completely melted.",
            "Preheat the grill for high heat.",
            "Lightly oil the grill grate. Discard marinade, and place chicken on the grill. Cook 6 to 8 minutes per side, until juices run clear.",
            "In a large glass bowl, stir together the vinegar, oil, soy sauce, lime juice, lemon juice, sherry, mustard, and honey. Mix in the garlic, brown sugar, lemon pepper, oregano, rosemary, and salt. Place the chicken in the mixture. Cover, and marinate in the refrigerator 8 hours or overnight.",
            "Spoon a rounded 1/2 cup bean mixture down the center of each tortilla. Fold sides over filling and roll up. Place enchiladas seam side down in baking dish; spoon salsa over each tortilla. Cover baking dish with aluminum foil.",
            "Bake in preheated oven for 25 minutes. Uncover and sprinkle with cilantro and 1/4 cup Cheddar cheese. Bake until cheese is melted, 2 to 3 minutes.",
            "Heat sesame oil in a large skillet over medium heat; cook and stir carrot and zucchini in the hot oil until vegetables begin to soften, about 5 minutes. Stir in bean sprouts, bamboo shoots, and mushrooms. Cook and stir until carrots are tender, about 5 more minutes. Season to taste with salt and set vegetables aside.",
            "To serve, divide hot cooked rice mixture between 3 serving bowls and top each bowl with 1/3 of the vegetable mixture and a fried egg. Serve sweet red chili sauce on the side for mixing into bibimbap.",
            "Stir cooked rice, green onions, soy sauce, and black pepper in the same skillet until the rice is hot. In a separate skillet over medium heat, melt butter and gently fry eggs, turning once, until the yolks are still slightly runny but the egg whites are firm, about 3 minutes per egg.",

        ]
        selected_steps = sample(xrange(len(steps)), randint(3, 6))
        selected_steps_array = list( steps[i] for i in selected_steps )
        recipe_names = [
            "The Best Parmesan Chicken Bake",
            "Chicken Parmigiana",
            "Ray's Chicken",
            "Black Bean and Rice Enchiladas",
            "Vegetarian Korma",
            "Vegetarian Bibimbap",
            "French Veggie Loaf",
            "Sunday Vegetarian Strata",
            "Overnight Asparagus Mushroom Strata",
            "Mom's Applesauce Pancakes",
            "Slow Cooker Belgian Chicken Booyah",
            "Poulet Parisienne",
            "Ham Casserole",
            "Scrambled Eggs Done Right",
            "Lasagna Roll Ups",
            "Bacon Wrapped Chicken",
            "Shrimp Francesca",
            "Crispy Baked Chicken",
            "Skillet Pork Chops with Potatoes and Onion",
            "Shrimp Scampi",
            "Grilled Portobellos Sauteed in Wine",
            "Cauliflower Au Gratin",
            "Zesty Apple Salad",
            "Great Pumpkin Dessert"
        ]
        steps_json = json.dumps(selected_steps_array)
        for j in range(1,4):
            title = recipe_names[randint(0, len(recipe_names)-1)]
            description = "This is one of my all-time favourite recipes. I just love " + title + " on weekends!"
            # ingredients = range((i-1) * 10 + (j-1) * 5, (i-1) * 10 + (j-1) * 5 + 5 )
            key = (i-1) * 3 + j
            average_rating = randint(1,4) + 0.23
            ingredients = sample(xrange(1, 950), randint(3,6))
            # Create the related RecipeIngredient fixtures
            for k in ingredients:
                entry = dict(
                    model = 'main.recipeingredient',
                    pk = (i-1)*10 + (i-1)*6*4 + (j-1)*4 + k, # Ok??
                    fields = dict(
                        recipe = key,
                        #ingredient = sample(xrange(1000), 1)[0],
                        ingredient = k,
                        amount = randint(2, 20)
                    )
                )
                data.append(entry)

            entry = dict(
                model = 'main.recipe',
                pk = key,
                fields = dict(
                    title = title,
                    description = description,
                    servings = i,
                    duration = str(duration),
                    image_url = image_url,
                    steps = steps_json,
                    creator = i,
                    creation_date = "2016-02-02",
                    creation_time = "09:23:15",
                    #ingredients = ingredients,
                    rating_count = i * j,
                    average_rating = average_rating
                )
            )
            data.append(entry)

    json.dump(data, outfile, indent = 4)

