# 10 user accounts are created, user1-user10, their passwords are "password".
rm db.sqlite3 
python manage.py migrate
python manage.py loaddata main/fixtures/ingredients.json
python manage.py loaddata main/fixtures/others.json
