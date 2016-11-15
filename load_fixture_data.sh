# 10 user accounts are created, user1-user10, their passwords are "password".
rm db.sqlite3 
python manage.py migrate
python manage.py loaddata main/fixtures/ingredients_2016-11-06_22_48_35.json
python manage.py loaddata main/fixtures/others_2016-11-11_14_19_46.json
