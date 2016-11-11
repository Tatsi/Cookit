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
        history_recipes = range(1, i)
        ingredients = range(10*(i-1)+1, 8 + 10 * (i - 1)+1 )

        # Create the actual User Accounts
        entry = dict(
            model = 'main.useraccount',
            pk = i,
            fields = dict(
                user = i,
                favourite_users = favourite_users,
                favourite_recipes = favourite_recipes,
                history_recipes = history_recipes
                #ingredients = ingredients
            )
        )
        data.append(entry)

        # Create the related UserIngredients
        for x in ingredients:
            entry = dict(
                model = 'main.useringredient',
                pk = x,
                fields = dict(
                    user_account = i,
                    ingredient = 1026,
                    amount = str(i * x) + "g",
                    infinite = False
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
            "Mix them and season with salt and pepper.",
            "Fry them in a frying pan for 20 minutes.",
            "Enjoy your delicious meal!",
        ]
        steps = json.dumps(steps)
        for j in range(1,4):
            title = "Recipe number " + str(i)
            description = "This is the description of recipe" + str(i) + ". It is very tasty and simple."
            ingredients = range((i-1) * 10 + (j-1) * 5, (i-1) * 10 + (j-1) * 5 + 5 )
            key = (i-1) * 3 + j-1
            average_rating = 3.232323232

            # Create the related RecipeIngredient fixtures
            for k in ingredients:
                entry = dict(
                    model = 'main.recipeingredient',
                    pk = k,
                    fields = dict(
                        recipe = key,
                        #ingredient = sample(xrange(1000), 1)[0],
                        ingredient = 4053,
                        amount = str(k) + " cup"
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
                    steps = steps,
                    creator = i,
                    #ingredients = ingredients,
                    rating_count = i * j,
                    average_rating = average_rating
                )
            )
            data.append(entry)




    json.dump(data, outfile, indent = 4)

